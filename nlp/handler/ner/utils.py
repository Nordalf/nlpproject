import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

import torch
from torch import nn
from torch.utils.data.dataset import Dataset

from transformers import PreTrainedTokenizer, torch_distributed_zero_first

logger = logging.getLogger(__name__)

@dataclass
class InputExample(object):
    """
    A single training/test example for token classification.
    Args:
        guid: Unique id for the example.
        words: list. The words of the sequence.
        labels: (Optional) list. The labels for each word of the sequence. This should be
        specified for train and dev examples, but not for test examples.
    """
    guid: str
    words: List[str]
    labels: Optional[List[str]]

@dataclass
class InputFeatures(object):
    """
    A single set of features of data.
    Args:
        input_ids: Indices of input sequence tokens in the vocabulary
        attention_mask: Mask to avoid performing attention on padding token indices. The Mask values
        are selected in the sequence [0, 1], where 1 is used for tokens that are NOT MASKED, and 0 for masked Tokens. 
        token_type_ids: Segment token indices to indicate first and second portions of the inputs. Indices are either set as [0, 1], where 0 is sentence A and 1 is sentence B.
        label_ids: Indices of labels in the range [0, len(label_list)]
    """

    input_ids: List[int]
    attention_mask: List[int]
    token_type_ids: Optional[List[int]] = None
    label_ids: Optional[List[int]] = None

class Split(Enum):
    train = "train"
    dev = "dev"
    test = "test"

class NerDataset(Dataset):
    features: List[InputFeatures]
    pad_token_label_id: int = nn.CrossEntropyLoss().ignore_index

    def __init__(
        self,
        data_dir: str,
        tokenizer: PreTrainedTokenizer,
        labels: List[str],
        model_type: str,
        max_seq_length: Optional[int] = None,
        overwrite_cache = False,
        mode: Split = Split.train,
        local_rank=-1,
        to_predict: Optional[str] = None
    ):
        # Load data features from cache or dataset file
        cached_features_file = os.path.join(
            data_dir, "cached_{}_{}_{}".format(mode, tokenizer.__class__.__name__, str(max_seq_length)),
        )

        if not to_predict:
            examples = read_examples_from_file(data_dir, mode)
        else:           
            examples = [InputExample(i, sentence.split(), [labels[0] for word in sentence.split()]) for i, sentence in enumerate(to_predict)]

        # The below is stated to ensure only one process executes the dataset. If this is not set, 
        # we do have a posibility of messing up with the dataset during training
        with torch_distributed_zero_first(local_rank):
            # If a cache file of the features exists, load it into PyTorch
            if os.path.exists(cached_features_file) and not overwrite_cache:
                logger.info(f"Loading features from cached file {cached_features_file}")
                self.features = torch.load(cached_features_file)
            else:
                logger.info(f"Converting features from dataset file at {data_dir}")
                self.features = convert_examples_to_features(
                    examples,
                    labels,
                    max_seq_length,
                    tokenizer,
                    cls_token_at_end=bool(model_type in ["xlnet"]),
                    # xlnet has a cls token at the end
                    cls_token=tokenizer.cls_token,
                    cls_token_segment_id=2 if model_type in ["xlnet"] else 0,
                    sep_token=tokenizer.sep_token,
                    sep_token_extra=bool(model_type in ["roberta"]),
                    # roberta uses an extra separator b/w pairs of sentences, cf. github.com/pytorch/fairseq/commit/1684e166e3da03f5b600dbb7855cb98ddfcd0805
                    pad_on_left=bool(tokenizer.padding_side == "left"),
                    pad_token=tokenizer.pad_token_id,
                    pad_token_segment_id=tokenizer.pad_token_type_id,
                    pad_token_label_id=self.pad_token_label_id,
                )
                if local_rank in [-1, 0]:
                    logger.info(f"Saving features into cached file {cached_features_file}")
                    torch.save(self.features, cached_features_file)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, i) -> InputFeatures:
        return self.features[i]

def read_examples_from_file(data_dir, mode: Union[Split, str]) -> List[InputExample]:
    """
        Reads through the example file and splits on space. 
        The first index in the splitted array is the word, where the second index is the label. If no label is defined, 'O' is inserted
        returns a list of input examples
    """
    if isinstance(mode, Split):
        mode = mode.value
    file_path = os.path.join(data_dir, f"{mode}.txt")
    guid_index = 1 # starting point
    examples = []
    with open(file_path, encoding='utf-8') as file:
        words = []
        labels = []
        for line in file:
            if line.startswith("-DOCSTART-") or line == "" or line == "\n" or line == "\r":
                if words:
                    examples.append(InputExample(guid=f"{mode}-{guid_index}", words=words, labels=labels))
                    guid_index += 1
                    words = []
                    labels = []
            else:
                splits = line.split(" ")
                words.append(splits[0])
                if len(splits) > 1:
                    labels.append(splits[-1].replace("\n", ""))
                else:
                    # Examples could have no label for mode = "test"
                    labels.append("O")
        if words:
            examples.append(InputExample(guid=f"{mode}-{guid_index}", words=words, labels=labels))

    return examples

def convert_examples_to_features(
    examples: List[InputExample],
    label_lists: List[str],
    max_seq_length: int,
    tokenizer: PreTrainedTokenizer, 
    cls_token_at_end=False,
    cls_token="[CLS]",
    cls_token_segment_id=1, 
    sep_token="[SEP]",
    sep_token_extra=False,
    pad_on_left=False,
    pad_token=0,
    pad_token_segment_id=0,
    pad_token_label_id=100,
    sequence_a_segment_id=0,
    mask_padding_with_zero=False,
) -> List[InputFeatures]:
    """
        Loads a data file into a list of InputFeatures. 
        The cls_token_at_end defines the location of the CLS token:
            False (default, BERT/XLM pattern): [CLS] + A + [SEP] + B + [SEP]
            True (XLNet/GPT pattern): A + [SEP] + B + [SEP] + [CLS]
        cls_token_segment_id defines the segment id associated to the CLS token (0 for BERT, 2 for XLNet)
    """
    label_map = {label: i for i, label in enumerate(label_lists)}
    
    features = []
    # Loop through the examples. They come from the dataset provided to the class.
    for (ex_index, example) in enumerate(examples):
        if ex_index % 10_000 == 0:
            logger.info(f"Writing example {ex_index} of {len(examples)}")

        tokens = []
        label_ids = []
        # Get the words and the labels and tokenize each word
        for word, label in zip(example.words, example.labels):
            word_tokens = tokenizer.tokenize(word)
            tokens.extend(word_tokens)

            # In some pretrained models (e.g. bert-base-multilingual), there is a chance the output is [] when calling tokenize with just a space
            # Therefore, a condition is determining the length, and then extending the tokens list with the word_tokens
            if len(word_tokens) > 0:
                label_ids.extend([label_map[label]] + [pad_token_label_id] * (len(word_tokens) - 1))

        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids:   0   0  0    0    0     0       0   0   1  1  1  1   1   1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids:   0   0   0   0  0     0   0
        
        # Append the seperate token to the end
        tokens += [sep_token]
        # Append the pad token label id at the end
        label_ids += [pad_token_label_id]
        # Create a list of type_ids  
        segment_ids = [sequence_a_segment_id] * len(tokens)

        if cls_token_at_end:
            tokens += [cls_token]
            label_ids += [pad_token_label_id]
            segment_ids = [sequence_a_segment_id] * len(tokens)
        else:
            # The BERT way with a CLS token first and then the tokens
            tokens = [cls_token] + tokens
            label_ids = [pad_token_label_id] + label_ids
            segment_ids = [cls_token_segment_id] + segment_ids

        # Use the tokenizer function to convert the tokens to ids for the word_embedding
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        
        # The maskhas 1 for real tokens and 0 for padding tokens. Only real tokens are attended to
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length either before the sequence or after
        padding_length = max_seq_length - len(input_ids)
        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            input_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + input_mask
            segment_ids = ([pad_token_segment_id * padding_length]) + segment_ids
            label_ids = ([pad_token_label_id] * padding_length) + label_ids
        else:
            input_ids += [pad_token] * padding_length
            input_mask += [0 if mask_padding_with_zero else 1] * padding_length
            segment_ids += [pad_token_segment_id] * padding_length
            label_ids += [pad_token_label_id] * padding_length

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        if ex_index < 5:
            logger.info("*** Example ***")
            logger.info("guid: %s", example.guid)
            logger.info("tokens: %s", " ".join([str(x) for x in tokens]))
            logger.info("input_ids: %s", " ".join([str(x) for x in input_ids]))
            logger.info("input_mask: %s", " ".join([str(x) for x in input_mask]))
            logger.info("segment_ids: %s", " ".join([str(x) for x in segment_ids]))
            logger.info("label_ids: %s", " ".join([str(x) for x in label_ids]))

        if "token_type_ids" not in tokenizer.model_input_names:
            segment_ids = None

        # Append the collected lists to the feature list and start over with the next example
        
        features.append(InputFeatures(input_ids=input_ids, attention_mask=input_mask, token_type_ids=segment_ids, label_ids=label_ids))

    return features

def get_labels(path:str) -> List[str]:
    """
        Get the defined labels in a list. If not defined, a default list of labels for NER is set
    """
    if path:
        with open(path, "r") as file:
            labels = file.read().splitlines()
        if "O" not in labels:
            # This label is indicating words outside entities to recognize and in this case has to be defined
            labels = ["O"] + labels
            
        return labels
    else:
        return ["O", "B-MISC", "I-MISC", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-GEO", "I-GEO"]
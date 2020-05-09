import logging
import os

import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score
from torch import nn, argmax
from typing import List, Dict, Tuple

from transformers import (
    AutoConfig, 
    AutoModelForTokenClassification,
    AutoTokenizer,
    EvalPrediction,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)

from .utils import NerDataset, Split, get_labels
from .arguments import ModelArguments, DataTrainingArguments

logger = logging.getLogger(__name__)


class NER:
    def __init__(self, model_name_or_path, labels, fine_tuned_model=None):
        self.model_args = ModelArguments(model_name_or_path='bert-base-multilingual-cased')
        self.data_args = DataTrainingArguments(data_dir="ner/datadir/", labels=labels)
        self.training_args = TrainingArguments(output_dir="testing-model", num_train_epochs=3, per_gpu_eval_batch_size=32, save_steps=750, seed=1)
        self.labels = get_labels(self.data_args.labels)
        self.label_map: Dict[int, str] = {i: label for i, label in enumerate(self.labels)}
        num_labels = len(self.labels)

        # Load pretrained model and tokenizer. Most pretrained models are provided by Google. 
        # The function .from_pretraining provided by HuggingFace guarantee only one process downloads the model and vocabulary

        self.config = AutoConfig.from_pretrained(
            self.model_args.config_name if self.model_args.config_name else self.model_args.model_name_or_path,
            num_labels=num_labels,
            id2label=self.label_map,
            label2id={label: i for i, label in enumerate(self.labels)},
            cache_dir=self.model_args.cache_dir,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_args.tokenizer_name if self.model_args.tokenizer_name else self.model_args.model_name_or_path,
            cache_dir=self.model_args.cache_dir,
            use_fase=self.model_args.use_fast,
        )
        self.model = AutoModelForTokenClassification.from_pretrained(
            fine_tuned_model,
            from_tf=bool(".ckpt" in self.model_args.model_name_or_path),
            config=self.config,
            cache_dir=self.model_args.cache_dir,
        )

    def train(self):
        if (
            os.path.exists(self.training_args.output_dir)
            and os.listdir(self.training_args.output_dir)
            and not self.training_args.overwrite_output_dir
        ):
            raise ValueError(
                f"Output directory ({self.training_args.output_dir}) already exists and is not empty. Use --overwrite_output_dir to overwrite"
            )

        # Setup logging
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=logging.INFO if self.training_args.local_rank in [-1, 0] else logging.WARN,
        )
        logger.warning(
            "Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
            self.training_args.local_rank,
            self.training_args.device,
            self.training_args.n_gpu,
            bool(self.training_args.local_rank != -1),
            self.training_args.fp16,
        )
        logger.info("Training/evaluation parameters %s", self.training_args)

        # Set seed for reproducebility
        set_seed(self.training_args.seed)

        # Get the labels and prepare the label_map
        
        # Get and split the dataset into train and eval
        self.training_args.do_train = True
        train_dataset = (
            NerDataset(
                data_dir=self.data_args.data_dir,
                tokenizer=self.tokenizer,
                labels=self.labels,
                model_type=self.config.model_type,
                max_seq_length=self.data_args.max_seq_length,
                overwrite_cache=self.data_args.overwrite_cache,
                mode=Split.train,
                local_rank=self.training_args.local_rank,
            )
            if self.training_args.do_train
            else None
        )
        eval_dataset = (
            NerDataset(
                data_dir=self.data_args.data_dir,
                tokenizer=self.tokenizer,
                labels=self.labels,
                model_type=self.config.model_type,
                max_seq_length=self.data_args.max_seq_length,
                overwrite_cache=self.data_args.overwrite_cache,
                mode=Split.dev,
                local_rank=self.training_args.local_rank,
            )
            if self.training_args.do_eval
            else None
        )

        # Initialize the Trainer class
        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            compute_metrics=self.compute_metrics,
        )

        # Start training
        trainer.train(
            model_path=self.model_args.model_name_or_path if os.path.isdir(self.model_args.model_name_or_path) else None
        )

        trainer.save_model()
        # Save the tokenizer to the same directory, so it is easier to share with others
        if trainer.is_world_master():
            self.tokenizer.save_pretrained(self.training_args.output_dir)


        
    def predict(self, sequence) -> Tuple[List[int]]:
        # Decode and encode to include special tokens in the string
        tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(sequence)))
        inputs = self.tokenizer.encode(sequence, return_tensors="pt")

        outputs = self.model(inputs)[0]
        predictions = np.argmax(outputs.detach().cpu().numpy(), axis=2)
        batch_size, seq_len = predictions.shape

        preds_list = [[] for _ in range(batch_size)]

        for i in range(batch_size):
            for j in range(seq_len):
                if '##' not in tokens[j]:
                    preds_list[i].append(self.label_map[predictions[i][j]])

        sentence = self.tokenizer.decode(self.tokenizer.encode(sequence), clean_up_tokenization_spaces=False)
        result = [dict(zip(('word', 'tag'), (token, prediction))) for token, prediction in zip(sentence.split(), preds_list[0])]
        return result

    def align_predictions(self, predictions: np.ndarray, label_ids: np.ndarray, label_map: Dict[int, str]) -> Tuple[List[int], List[int]]:
        
        preds = argmax(predictions, axis=2)
        batch_size, seq_len = preds.shape

        out_label_list = [[] for _ in range(batch_size)]
        preds_list = [[] for _ in range(batch_size)]

        print(label_map)

        for i in range(batch_size):
            for j in range(seq_len):
                out_label_list[i].append(label_map[predictions[i][j]])
                print(out_label_list)
                preds_list[i].append(label_map[preds[i][j]])

        return preds_list, out_label_list

    def compute_metrics(self, p: EvalPrediction) -> Dict:
            preds_list, out_label_list = self.align_predictions(p.predictions, p.label_ids, label_map=self.label_map)
            return {
                "Precision": precision_score(out_label_list, preds_list),
                "Recall": recall_score(out_label_list, preds_list),
                "F1-Score": f1_score(out_label_list, preds_list)
            }

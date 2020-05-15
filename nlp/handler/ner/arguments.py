from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from transformers import MODEL_WITH_LM_HEAD_MAPPING


MODEL_CONFIG_CLASSES = list(MODEL_WITH_LM_HEAD_MAPPING.keys())
MODEL_TYPES = tuple(conf.model_type for conf in MODEL_CONFIG_CLASSES)

@dataclass
class ModelArguments:
    """
        Arguments pertaining to which model/config/tokenizer we are going to fine-tune from
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier"}
    )

    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )

    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )

    model_type: Optional[str] = field(
        default=None,
        metadata={"help": "If training from scratch, pass a model type from the list: " + ", ".join(MODEL_TYPES)},
    )

    use_fast: bool = field(default=False, metadata={"help": "Set this flag to use fast tokenization"})
    
    cache_dir: Optional[str] = field (
        default=None, metadata={"help": "The path to store the pretrained models"}
    )

@dataclass
class DataTrainingArguments:
    """
        Arguments pertaining to waht data we are going to input our model for training and eval
    """

    train_data_file: Optional[str] = field(
        default=None, metadata={"help": "The input training data file (a text file)."}
    )

    eval_data_file: Optional[str] = field(
        default=None,
        metadata={"help": "An optional input evaluation data file to evaluate the perplexity on (a text file)."},
    )

    labels: Optional[str] = field (
        default="./labels.txt",
        metadata={"help": "Path to the file containing all the labels. If not specified, defaults are used"}
    )

    max_seq_length: int = field (
        default=128,
        metadata={"help": "The maximum total input sequence length after tokenization. Sequences longer than this is truncated. Sequences shorter is padded"}
    )

    overwrite_cache: bool = field(
        default=False,
        metadata={"help": "Overwrite the cached training and evaluation sets"}
    )

    line_by_line:bool = field(
        default=False,
        metadata={"help": "Whether distinct lines of text in the dataset are to be handled as distinct sequences."}
    )

    mlm: bool = field (
        default=False,
        metadata={"help": "Train with masked-language modeling loss instead of language modeling."}
    )

    mlm_probability: float = field(
        default=0.15, metadata={"help": "Ratio of tokens to mask for masked language modeling loss"}
    )
    block_size: int = field(
        default=-1,
        metadata={
            "help": "Optional input sequence length after tokenization."
            "The training dataset will be truncated in block of this size for training."
            "Default to the model max input length for single sentence inputs (take into account special tokens)."
        },
    )

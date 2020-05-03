from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


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

    use_fast: bool = field(default=False, metadata={"help": "Set this flag to use fast tokenization"})
    
    cache_dir: Optional[str] = field (
        default=None, metadata={"help": "The path to store the pretrained models"}
    )

@dataclass
class DataTrainingArguments:
    """
        Arguments pertaining to waht data we are going to input our model for training and eval
    """

    data_dir: str = field (
        metadata={"help": "The input data directory. Should contain the .txt files"}
    )

    labels: Optional[str] = field (
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

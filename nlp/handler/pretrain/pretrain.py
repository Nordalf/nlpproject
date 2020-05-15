import logging
from pathlib import Path
from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
import torch as nn
from torch.utils.data.dataset import Dataset
from ..ner.arguments import ModelArguments, DataTrainingArguments
from transformers import (
    AutoModelWithLMHead,
    AutoTokenizer,
    CONFIG_MAPPING,
    DataCollatorForLanguageModeling,
    LineByLineTextDataset,
    PreTrainedTokenizer,
    set_seed, 
    TextDataset,
    TrainingArguments,
    Trainer,
)


logger = logging.getLogger(__name__)


class DanDataset(Dataset):
    def __init__(self, evaluate: bool = False):
        self.model_args = ModelArguments(model_name_or_path=None, model_type='bert', tokenizer_name='models/danbert-small/vocab.json', config_name="models/danbert-small/config.json")
        self.data_args = DataTrainingArguments(train_data_file="handler/datadir/da-train.txt", eval_data_file="handler/datadir/da-eval.txt", labels="handler/datadir/labels.txt", mlm=True, line_by_line=True)
        self.training_args = TrainingArguments(output_dir="models/danbert-small", num_train_epochs=3, per_gpu_eval_batch_size=8, save_steps=750, seed=42, learning_rate=1e-4, save_total_limit=2)

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

        set_seed(self.training_args.seed)

        config = CONFIG_MAPPING[self.model_args.model_type]()
        logger.warning("You are instantiating a new config instance from scratch.")

        tokenizer = AutoTokenizer.from_pretrained('models/danbert-small')

        model = AutoModelWithLMHead.from_config(config)

        # model.resize_token_embeddings(len(tokenizer))

        if self.data_args.block_size <= 0:
            self.data_args.block_size = 512
        # Our input block size will be the max possible for the model
        else:
            self.data_args.block_size = min(self.data_args.block_size, 512)

        train_dataset = (
            self.get_dataset(self.data_args, tokenizer=tokenizer, local_rank=self.training_args.local_rank, evaluate=True)
        )

        eval_dataset = (
            self.get_dataset(self.data_args, tokenizer=tokenizer, local_rank=self.training_args.local_rank, evaluate=True)
        )

        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=self.data_args.mlm, mlm_probability=self.data_args.mlm_probability)

        trainer = Trainer(
            model=model,
            args=self.training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            # eval_dataset=eval_dataset,
            prediction_loss_only=True,
        )

        trainer.train(model_path=None)
        trainer.save_model()

    def get_dataset(self, args: DataTrainingArguments, tokenizer: PreTrainedTokenizer, evaluate=False, local_rank=-1):
        file_path = args.eval_data_file if evaluate else args.train_data_file
        if args.line_by_line:
            return LineByLineTextDataset(
                tokenizer=tokenizer, file_path=file_path, block_size=args.block_size, local_rank=local_rank
            )
        else:
            return TextDataset(
                tokenizer=tokenizer, file_path=file_path, block_size=args.block_size, local_rank=local_rank,
            )

class Pretrain:
    def __init__(self):
        print("Pretraining started")
        self.pretrain_tokenization()
    
    def pretrain_tokenization(self):
        paths = [str(x) for x in Path("handler/datadir/").glob("*-train.txt")]
        print(paths)
        tokenizer = ByteLevelBPETokenizer()

        tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"])

        tokenizer.save(".", "danbert-small")

    def pretrain(self):
        self.pretrain_tokenization()
        dataset = DanDataset(evaluate=True)

def main():
    DanDataset(evaluate=False)

if __name__ == "__main__":
    main()


from pathlib import Path
from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
import torch as nn
from torch.utils.data.dataset import Dataset
from ..ner.arguments import ModelArguments, DataTrainingArguments
from transformers import TrainingArguments


class DanDataset(Dataset):
    def __init__(self, evaluate: bool = False):
        self.model_args = ModelArguments(model_name_or_path=None)
        self.data_args = DataTrainingArguments(data_dir="handler/datadir/", labels="handler/datadir/labels.txt")
        self.training_args = TrainingArguments(output_dir="models/danbert-small", num_train_epochs=3, per_gpu_eval_batch_size=32, save_steps=750, seed=1)

        tokenizer = ByteLevelBPETokenizer("models/danbert-small/vocab.json", "models/danbert-small/merges.txt")
        tokenizer.post_processor = BertProcessing(("</s>", tokenizer.token_to_id("</s>")),("<se>", tokenizer.token_to_id("<se>")))
        tokenizer.enable_truncation(max_length=512)
        self.examples = []

        src_files = Path("handler/datadir/").glob("*-eval.txt") if evaluate else  Path("handler/datadir/").glob("*-train.txt")

        for src_file in src_files:
            lines = src_file.read_text(encoding="utf-8").splitlines()
            self.examples += [x.ids for x in tokenizer.encode_batch(lines)]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return nn.tensor(self.examples[i])


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


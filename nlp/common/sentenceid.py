import os
import pandas as pd
import csv
import re

sentence_id = 0

with open("../data/dk_ner_train.tsv", 'r+', encoding='utf-8') as fp:
    lines = fp.read().splitlines()

# (?!\d+)[\t ](?=\d+\w) - match steder hvor punktum mangler i tal

# Used for adding sentence ids
with open("../data/dk_ner_train.tsv", 'w', encoding='utf-8') as fp:
    for line in lines:
        print(f'{sentence_id}\t{line}', file=fp)
        if re.search(r'\.(?!(\w+))', line):
            sentence_id += 1

# with open("train_dklower1.csv", 'r+', encoding='utf-8') as fp:
#     lines = fp.read().splitlines()

# with open("train_dklower2.csv", 'w', encoding='utf-8') as fp:
#     for line in lines:
#         if re.search(r'(?!\d+)[\t\s](?=\d+\w)', line):
#             newline = re.sub(r'(?!\d+)[\t\s](?=\d+\w\t)', '.', line)r
#             print(f'{newline}', file=fp)
#         else:
#             print(f'{line}', file=fp)

# with open("train_dklower2.csv", 'r', encoding='utf-8') as file:
#     corpus = pd.read_csv(file, delimiter='\t')
#     print(corpus.head(100))
    
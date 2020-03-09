import os
import pandas as pd
import csv
import re

sentence_id = 0

with open("processedfiles/danish_bio_train.tsv", 'r+', encoding='utf-8') as fp:
    lines = fp.read().splitlines()

# (?!\d+)[\t ](?=\d+\w) - match steder hvor punktum mangler i tal

# Used for adding sentence ids
with open("processedfiles/danish_bio_train.tsv", 'w', encoding='utf-8') as fp:
    for line in lines:
        print(f'{sentence_id}\t{line}', file=fp)
        if re.search(r'\.(?!(\w+))', line):
            sentence_id += 1

sentence_id = 0
with open("processedfiles/danish_bio_eval.tsv", 'r+', encoding='utf-8') as fp:
    lines = fp.read().splitlines()

# Used for adding sentence ids
with open("processedfiles/danish_bio_eval.tsv", 'w', encoding='utf-8') as fp:
    for line in lines:
        print(f'{sentence_id}\t{line}', file=fp)
        if re.search(r'\.(?!(\w+))', line):
            sentence_id += 1
import re

with open('dk_ner_eval.tsv', 'r', encoding='utf-8') as eval:
    lines = eval.read().splitlines()

with open('dk_ner_eval2.tsv', 'a', encoding='utf-8') as eval:
    for line in lines:
        line = re.sub('\t\w+\t', lambda m: m.group(0).lower(), line)
        print(f'{line}', file=eval)
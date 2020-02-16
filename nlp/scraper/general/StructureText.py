# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 14:44:08 2019

@author: alexf
"""

import re
import textwrap

with open("cleansed_version2.txt", "rt", encoding='utf-8') as infile:
    text = infile.read()
    text = re.sub(r'\.(?!(\s\d+)|\s+(jan|feb|mar|apr|maj|jun|juli|aug|sep|okt|nov|dec|i m)|(\w+(\.|))+)', r'\1\n', text, flags=re.IGNORECASE)
    text_no_leading_whitespace = ""
    for line in text.split('\n'):
        text_no_leading_whitespace += textwrap.dedent(line) + '\n'
        
with open('structured_cleansed_version2.txt', 'wt', encoding='utf-8') as outfile:
    outfile.write(text_no_leading_whitespace)
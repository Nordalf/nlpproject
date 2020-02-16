import os
import re
import fileinput

class TrainingPreprocessor:
    def __init__(self, file):
        self.file = file
        self.preprocess(self.file)
        self.sentence_split(self.file)
        
    def preprocess(self, file):
        '''Preprocess' the data which is used for training'''
        # Removes line having starting with a lot of spaces and digits
        with fileinput.FileInput(self.file, inplace=True, backup='.bak') as sed_file:
            for line in sed_file:
                # Removes leading whitespace and leading tabs
                if re.search(r"^\s+|^\t+", line):
                    print(re.sub(r"^\s+|^\t+", "", line), end='')

                # If bullet point lists, remove line
                if re.search(r"(^\s+\d+|^(\d{1,}[\.]\d+\s+\-|\d+\s+\w+))", line):
                    print(re.sub(r"(^\s+\d+|^(\d{1,}[\.]\d+\s+\-|\d+\s+\w+)).*$", "", line), end='')
                    continue

                 # If a line starts with ":", "*", or "-", then the characters and trailing spaces are replaced by nothing. 
                if re.search(r"^\*\s+|^\:\s+|^\-\s+", line):
                    print(re.sub(r"^\*\s+|^\:\s+|^\-\s+", "", line), end='')

                # Match URL's for HTTP/HTTPS
                if re.search(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", line):
                    print(re.sub(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", "", line), end='')

    def sentence_split(self, file):
        # Removes line having starting with a lot of spaces and digits
        with fileinput.FileInput(file, inplace=True, backup='.bak') as sed_file:
            for line in sed_file:
                print(re.sub(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", ".\n", line), end='')

    def format_traning_data():
        '''Formats preprocessed data into the BIO format. This is to be used for training the language model'''




# Fjern *: i starten af saetninger : sed -E 's/^\*.|^\:.//g' < drdkcorpus.txt > drdkcorpus1.txt

# \.(?!\d+|\w+|\S|\.|\s[a-z]) En saetning for hver linje
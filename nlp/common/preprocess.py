import os
import re
import fileinput

from common.bio import BIOFILE

class TrainingPreprocessor:
    def __init__(self, file):
        self.file = file
        self.preprocess(self.file)
        
    def preprocess(self, file):
        '''Preprocess' the data which is used for training'''
        # Removes line having starting with a lot of spaces and digits
        # with open(self.file, "r+", encoding='utf-8') as sed_file:
        #     lines = sed_file.read().splitlines()
        # with open(self.file, "w", encoding='utf-8') as sed_file:
        #     activated = False
        #     for line in lines:
        #         # Removes leading whitespace and leading tabs
        #         if re.search(r"\s{2,}", line):
        #             line = re.sub(r"\s{2,}", " ", line)
        #             print(f"{line}", file=sed_file)
        #             activated = True

        #         if re.search(r"^\s+|^\t+", line):
        #             line = re.sub(r"^\s+|^\t+", "", line)
        #             print(f"{line}", file=sed_file)
        #             activated = True

        #         # If bullet point lists, remove line
        #         if re.search(r"(^\s+\d+|^(\d{1,}[\.]\d+\s+\-|\d+\s+\w+))", line):
        #             line = re.sub(r"(^\s+\d+|^(\d{1,}[\.]\d+\s+\-|\d+\s+\w+)).*$", "", line)
        #             print(f"{line}", file=sed_file)
        #             activated = True

        #         # If a line starts with ":", "*", or "-", then the characters and trailing spaces are replaced by nothing. 
        #         if re.search(r"^\*\s+|^\:\s+|^\-\s+", line):
        #             print(re.sub(r"^\*\s+|^\:\s+|^\-\s+", "", line), file=sed_file)
        #             activated = True

        #         # Match URL's for HTTP/HTTPS
        #         if re.search(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", line):
        #             line = re.sub(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", "", line)
        #             print(f"{line}", file=sed_file)
        #             activated = True   

        #         if not activated:
        #             print(f"{line}", file=sed_file)
                
        #         activated = False

        # self.sentence_split(file)
        self.format_traning_data(file)

    def sentence_split(self, file):
        # Remove lines starting with multiple spaces and digits
        with open(file, "r+", encoding='utf-8') as sed_file:
            lines = sed_file.read().splitlines()
        with open(file, "w", encoding='utf-8') as sed_file:
            for line in lines:
                line = re.sub(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", ".\n", line)
                print(f"{line}", file=sed_file, end='')
        with open(file, "r+", encoding='utf-8') as sed_file:
            lines = sed_file.read().splitlines()
        with open(file, "w", encoding='utf-8') as sed_file:
            for line in lines:
                line = re.sub(r"^\s+|^\t+", "", line)
                print(f"{line}", file=sed_file)

    def format_traning_data(self, file):
        '''Formats preprocessed data into the BIO format. This is to be used for training the language model'''
        BIOFILE(file)



# Fjern *: i starten af saetninger : sed -E 's/^\*.|^\:.//g' < drdkcorpus.txt > drdkcorpus1.txt

# \.(?!\d+|\w+|\S|\.|\s[a-z]) En saetning for hver linje
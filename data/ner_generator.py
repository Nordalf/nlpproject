import csv
import os
import re

drengenavne_map = {}
# Danish Male Names Mapping
with open("GodkendteDrengeNavne.txt", 'r') as gdn:
    for line in gdn:
        line = line.rstrip()
        drengenavne_map[line] = line

pigenavne_map = {}
# Danish Female Names Mapping
with open("GodkendtePigeNavne.txt", 'r') as gpn:
    for line in gpn:
        line = line.rstrip()
        pigenavne_map[line] = line

unisexnavne_map = {}
# Danish Unisex Names Mapping
with open("GodkendteUnisexNavne.txt", 'r') as gun:
    for line in gun:
        line = line.rstrip()
        unisexnavne_map[line] = line

bynavn_map = {}
# Danish City Names Mapping
with open("Bynavne.txt", 'r', encoding="utf8") as bn:
    for line in bn:
        line = line.rstrip()
        bynavn_map[line] = line

landenavne_map = {}
# Country Names Mapping
with open("Landenavne.txt", 'r') as ln:
    for line in ln:
        line = line.rstrip()
        landenavne_map[line] = line

adresse_map = {}
# Country Names Mapping
with open("Adresser.txt", 'r', encoding="utf8") as adrfile:
    for line in adrfile:
        line = line.rstrip()
        adresse_map[line] = line

previous_was_person = False
previous_was_location = False

with open("drdkcorpus4.txt", "r+", encoding="utf-8") as readfile:
    with open("dk_ner_corpus.tsv", "a+", encoding="utf-8") as writefile:
        for line in readfile:
            splitted_line = line.split(' ')
            for word in splitted_line:
                if previous_was_person and word[0].isupper():
                    if word in drengenavne_map or word in pigenavne_map or word in unisexnavne_map:
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-PER" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                        else:
                            writefile.write(word + "\t" + "I-PER" + "\n")
                    elif word 

                    if word in drengenavne_map or word in pigenavne_map or word in unisexnavne_map:
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-PER" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                        else:
                            writefile.write(word + "\t" + "B-PER" + "\n")
                    elif word 
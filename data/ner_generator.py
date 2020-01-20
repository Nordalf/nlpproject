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

# PERSON
previous_was_person = False
punctuation_appeared_person = False
comma_appeared_person = False

# ADRESSE
previous_was_location = False
punctuation_appeared_location = False
comma_appeared_location = False

# BY
previous_was_city = False
punctuation_appeared_city = False
comma_appeared_city = False

# LAND
previous_was_country = False
punctuation_appeared_country = False
comma_appeared_country = False

with open("drdkcorpus4.txt", "r+", encoding="utf-8") as readfile:
    with open("dk_ner_corpus.tsv", "a+", encoding="utf-8") as writefile:
        for line in readfile:
            splitted_line = line.split(' ')
            for word in splitted_line:
                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis Hr. Falk.) eller forrige var en person
                if word[0].isupper() and (punctuation_appeared_person or previous_was_person or comma_appeared_person):
                    # Hvis ordet er et genkendt navn
                    if word in (drengenavne_map or pigenavne_map or unisexnavne_map):
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.|\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-PER" + "\n")
                        else:
                            writefile.write(word + "\t" + "I-PER" + "\n")
                            punctuation_appeared_person = False
                            comma_appeared_person = False
                    else:
                        previous_was_person = False
                        if punctuation_appeared_person:
                            punctuation_appeared_person = False
                            # Ordet før var en person og indeholdt et punktum, men var ikke et genkendt navn
                            writefile.write("." + "\t" + "O" + "\n")
                        if comma_appeared_person:
                            comma_appeared_person = False
                            # Ordet før var en person og indeholdt et komma, men var ikke et genkendt navn
                            writefile.write("," + "\t" + "O" + "\n")

                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis Gl. Byvej) eller forrige var en adresse
                elif word[0].isupper() and (punctuation_appeared_location or previous_was_location or comma_appeared_location):
                    # Hvis ordet er en genkendt adresse
                    if word in adresse_map:
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.|\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                        else:
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                            punctuation_appeared_location = False
                            comma_appeared_comma = False
                    else:
                        previous_was_location = False
                        if punctuation_appeared_location:
                            punctuation_appeared_location = False
                            # Ordet før var en adresse og indeholdt et punktum, men var ikke en genkendt adresse
                            writefile.write("." + "\t" + "O" + "\n")
                        if comma_appeared_location:
                            comma_appeared_location = False
                            # Ordet før var en adresse og indeholdt et komma, men var ikke en genkendt adresse
                            writefile.write("," + "\t" + "O" + "\n")


                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis ?? Tror sgu ikke der er nogen) eller forrige var by
                elif word[0].isupper() and (punctuation_appeared_city or previous_was_city or comma_appeared_city):
                    # Hvis ordet er en genkendt by
                    if word in bynavn_map:
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                        else:
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                            punctuation_appeared_city = False
                            comma_appeared_city = False
                    else:
                        previous_was_city = False
                        if punctuation_appeared_city:
                            punctuation_appeared_city = False
                            # Ordet før var en by og indeholdt et punktum, men var ikke en genkendt by
                            writefile.write("." + "\t" + "O" + "\n")
                        if comma_appeared_city:
                            comma_appeared_city = False
                            # Ordet før var en by og indeholdt et komma, men var ikke en genkendt by
                            writefile.write("," + "\t" + "O" + "\n")

                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis St. Lucia) eller forrige var et land
                elif word[0].isupper() and (punctuation_appeared_country or previous_was_country or comma_appeared_country):
                    # Hvis ordet er et genkendt land
                    if word in adresse_map:
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.|\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                        else:
                            writefile.write(word + "\t" + "I-LOC" + "\n")
                            punctuation_appeared_country = False
                            comma_appeared_country
                    else:
                        previous_was_country = False
                        if punctuation_appeared_country:
                            punctuation_appeared_country = False
                            # Ordet før var et land og indeholdt et punktum, men var ikke en genkendt land
                            writefile.write("." + "\t" + "O" + "\n")
                        if comma_appeared_country:
                            comma_appeared_country = False
                            # Ordet før var et land og indeholdt et komma, men var ikke en genkendt land
                            writefile.write("," + "\t" + "O" + "\n")
                else:
                    previous_was_person = False
                    # Hvis ordet er et genkendt navn
                    if word in (drengenavne_map or pigenavne_map or unisexnavne_map):
                        previous_was_person = True
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-PER" + "\n")
                            # Både en person og ender med et punktum
                            punctuation_appeared_person = True
                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-PER" + "\n")
                            # Både en person og ender med et punktum
                            comma_appeared_person = True
                        else:
                            writefile.write(word + "\t" + "B-PER" + "\n")
                            punctuation_appeared_person = False
                            comma_appeared_person = False

                    # Hvis ordet er en dansk adresse
                    elif word in adresse_map:
                        previous_was_location = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-LOC" + "\n")
                            punctuation_appeared_location = True
                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-LOC" + "\n")
                            comma_appeared_location = True
                        else:
                            writefile.write(word + "\t" + "B-LOC" + "\n")
                            punctuation_appeared_location = False
                            comma_appeared_location = False

                    # Hvis ordet er en dansk by
                    elif word in bynavn_map:
                        previous_was_city = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            punctuation_appeared_city = True
                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            comma_appeared_city = True
                        else:
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            punctuation_appeared_city = False
                            comma_appeared_city = False

                    # Hvis ordet er en dansk by
                    elif word in landenavne_map:
                        previous_was_country = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            punctuation_appeared_country = True
                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            comma_appeared_country = True
                        else:
                            writefile.write(word + "\t" + "B-GEO" + "\n")
                            punctuation_appeared_country = False
                            comma_appeared_country = False

                    else:
                        # Helt almindeligt ord. Ligeglad med at identificere det
                        writefile.write(word + "\t" + "O" + "\n")



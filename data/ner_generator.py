import csv
import os
import re
import string

drengenavne_map = {}
# Danish Male Names Mapping
with open("Godkendte_Drengenavne.csv", 'r', encoding='utf-8') as gdn:
    for line in gdn:
        line = line.rstrip()
        drengenavne_map[line] = line

def is_in_drengenavne(word):
    for w in drengenavne_map:
        if re.search(r'^' + w + '$', word):
            return True
    return False

pigenavne_map = {}
# Danish Female Names Mapping
with open("Godkendte_Pigenavne.csv", 'r', encoding='utf-8') as gpn:
    for line in gpn:
        line = line.rstrip()
        pigenavne_map[line] = line

def is_in_pigenavne(word):
    for w in pigenavne_map:
        if re.search(r'^' + w + '$', word):
            return True
    return False

# unisexnavne_map = {}
# # Danish Unisex Names Mapping
# with open("GodkendteUnisexNavne.txt", 'r') as gun:
#     for line in gun:
#         line = line.rstrip()
#         unisexnavne_map[line] = line

# def is_in_unisexnavne(word):
#     for w in unisexnavne_map:
#         if re.search(r'^' + w + '$', word):
#             return True
#     return False

bynavn_map = {}
# Danish City Names Mapping
with open("Bynavne.txt", 'r', encoding="utf-8") as bn:
    for line in bn:
        line = line.rstrip()
        bynavn_map[line] = line

landenavne_map = {}
# Country Names Mapping
with open("Landenavne.txt", 'r', encoding='utf-8') as ln:
    for line in ln:
        line = line.rstrip()
        landenavne_map[line] = line

adresse_map = {}
# Country Names Mapping
with open("Adresser.txt", 'r', encoding="utf=8") as adrfile:
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
    with open("dk_ner_corpus_bio.tsv", "a+", encoding="utf-8") as writefile:
        for line in readfile:
            splitted_line = line.split(' ')
            for word in splitted_line:
                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis Hr. Falk.) eller forrige var en person
                # person_condition = punctuation_appeared_person or previous_was_person or comma_appeared_person
                # location_condition = punctuation_appeared_location or previous_was_location or comma_appeared_location
                # city_condition = punctuation_appeared_city or previous_was_city or comma_appeared_city
                # country_condition = punctuation_appeared_country or previous_was_country or comma_appeared_country

                if previous_was_person:
                    if word[0].isupper():

                        if word not in adresse_map and word not in bynavn_map and word not in landenavne_map:
                            # Hvis ordet har et korrekt punktum som slutning på en sætning
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("Person med punktum I:", word)
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-PER" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("Person med komma I:", word)
                                writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-PER" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")

                            else:
                                writefile.write(word + "\t" + "I-PER" + "\n")
                                punctuation_appeared_person = False
                                comma_appeared_person = False
                                continue
                    
                    previous_was_person = False
                    punctuation_appeared_person = False
                    comma_appeared_person = False
                        
                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis Gl. Byvej) eller forrige var en adresse
                elif previous_was_location:
                    if word[0].isupper():
                    
                        if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:

                            # Hvis ordet har et korrekt punktum som slutning på en sætning
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-ADDR med punktum I:", word)
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-LOC" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-ADDR med komma I:", word)
                                writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-LOC" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")

                            else:
                                writefile.write(word + "\t" + "I-LOC" + "\n")

                    previous_was_location = False
                    punctuation_appeared_location = False
                    comma_appeared_location = False
                        
                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis ?? Tror sgu ikke der er nogen) eller forrige var by
                elif previous_was_city:
                    if word[0].isupper():
                        if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:
                            

                            # Hvis ordet har et korrekt punktum som slutning på en sætning
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-LOC med punktum I:", word)
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-LOC" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-LOC med komma I:", word)
                                writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-LOC" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")

                            else:
                                writefile.write(word + "\t" + "I-LOC" + "\n")

                    previous_was_city = False
                    punctuation_appeared_city = False
                    comma_appeared_city = False

                # Hvis stort bogstav, forrige ord sluttede med et punktum (Eksempelvis St. Lucia) eller forrige var et land
                elif previous_was_country:
                    if word[0].isupper():
                        if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:
                            
                            # Hvis ordet har et korrekt punktum som slutning på en sætning
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-GEO med punktum I:", word)
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-GEO" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                # print("I-GEO med komma I:", word)
                                writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-GEO" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")

                            else:
                                writefile.write(word + "\t" + "I-GEO" + "\n")

                    previous_was_country = False
                    punctuation_appeared_country = False
                    comma_appeared_country = False
                
                else:
                    previous_was_person = False
                    previous_was_location = False
                    previous_was_city = False
                    previous_was_country = False          

                    # Hvis ordet er et genkendt navn
                    # Ordet bliver trimmet for komma eller punktum, da hvis en genkendt entitet findes, men indeholder et af disse,
                    # så vil der ikke være et match, da "in" er eksakt
                    temp_word = word
                    if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                        temp_word = word.translate(str.maketrans('', '', string.punctuation))

                    if re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                        temp_word = word.replace(',', '')

                    if temp_word in drengenavne_map or temp_word in pigenavne_map:
                        previous_was_person = True
                        # Hvis ordet har et korrekt punktum som slutning på en sætning
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Person med punktum B:", word)
                            writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-PER" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                            previous_was_person = False

                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Person med komma B:", word)
                            writefile.write(word.replace(',', '') + "\t" + "B-PER" + "\n")
                            writefile.write("," + "\t" + "O" + "\n")
                            previous_was_person = False

                        else:
                            writefile.write(word + "\t" + "B-PER" + "\n")
                            punctuation_appeared_person = False
                            comma_appeared_person = False

                    # Hvis ordet er en dansk adresse
                    elif temp_word in adresse_map:
                        previous_was_location = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Lokation med punktum B:", word)
                            writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-LOC" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                            previous_was_location = False

                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Lokation med komma B:", word)
                            writefile.write(word.replace(',','') + "\t" + "B-LOC" + "\n")
                            writefile.write("," + "\t" + "O" + "\n")
                            previous_was_location = False

                        else:
                            writefile.write(word + "\t" + "B-LOC" + "\n")

                    # Hvis ordet er en dansk by
                    elif temp_word in bynavn_map:
                        previous_was_city = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("By med punktum B:", word)
                            writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-LOC" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                            previous_was_city = False

                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("By med komma B:", word)
                            writefile.write(word.replace(',', '') + "\t" + "B-LOC" + "\n")
                            writefile.write("," + "\t" + "O" + "\n")
                            previous_was_city = False
                            
                        else:
                            writefile.write(word + "\t" + "B-LOC" + "\n")

                    # Hvis ordet er en dansk by
                    elif temp_word in landenavne_map:
                        previous_was_country = True
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Land med punktum B:", word)
                            writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-GEO" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")
                            previous_was_country = False

                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            # print("Land med komma B:", word)
                            writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "B-GEO" + "\n")
                            writefile.write("," + "\t" + "O" + "\n")
                            previous_was_country = False

                        else:
                            writefile.write(word + "\t" + "B-GEO" + "\n")

                    else:
                        # Helt almindeligt ord. Ligeglad med at identificere det
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            word = word.rstrip("\n\r")
                            writefile.write(word.translate(str.maketrans('', '', string.punctuation)) + "\t" + "O" + "\n")
                            writefile.write("." + "\t" + "O" + "\n")

                        elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            writefile.write(word.replace(',', '') + "\t" + "O" + "\n")
                            writefile.write("," + "\t" + "O" + "\n")
                        else:
                            writefile.write(word + "\t" + "O" + "\n")



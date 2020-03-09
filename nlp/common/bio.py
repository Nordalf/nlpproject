import csv
import os
import re
import string

BIO_FOLDER = 'common/processedfiles/'
RESOURCE_FOLDER = 'resources/'

# Maps of known entities
drengenavne_map = {}
pigenavne_map = {}
bynavn_map = {}
landenavne_map = {}
adresse_map = {}

class BIOFILE:
    def __init__(self, file):
        self.file = file
        load_known_entities()
        preprocess(self.file)

def load_known_entities():
    # Danish Male Names Mapping
    with open(RESOURCE_FOLDER + "Godkendte_Drengenavne.csv", 'r', encoding='utf-8') as gdn:
        for line in gdn:
            line = line.rstrip()
            drengenavne_map[line] = line

    # Danish Female Names Mapping
    with open(RESOURCE_FOLDER + "Godkendte_Pigenavne.csv", 'r', encoding='utf-8') as gpn:
        for line in gpn:
            line = line.rstrip()
            pigenavne_map[line] = line

    # Danish City Names Mapping
    with open(RESOURCE_FOLDER + "Bynavne.txt", 'r', encoding="utf-8") as bn:
        for line in bn:
            line = line.rstrip()
            bynavn_map[line] = line

    # Country Names Mapping
    with open(RESOURCE_FOLDER + "Landenavne.txt", 'r', encoding='utf-8') as ln:
        for line in ln:
            line = line.rstrip()
            landenavne_map[line] = line

    # Country Names Mapping
    with open(RESOURCE_FOLDER + "Adresser.txt", 'r', encoding="utf=8") as adrfile:
        for line in adrfile:
            line = line.rstrip()
            adresse_map[line] = line

def preprocess(file):
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
    with open(file, "r+", encoding="utf-8") as readfile:
        with open(BIO_FOLDER + '/danish_bio.tsv', "a+", encoding="utf-8") as writefile:
            for line in readfile:
                splitted_line = line.split(' ')
                for word in splitted_line:
                    
                    if is_word_special_character(word, writefile):
                        continue

                    word = check_special_characters_named_entities_start(word, writefile)
                    word, special_character, special_character_found = check_special_characters_named_entities_end(word)
                    word, char_after, apostrophe_found = check_for_apostrophe(word)

                    # If big letter, previous word ended with a punctuation (e.g. Mr. Johnson), or previous was a person
                    if previous_was_person:
                        if word[0].isupper():

                            if word not in adresse_map and word not in bynavn_map and word not in landenavne_map:
                                # If the word has an ending punctuation of a sentence 
                                if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-PER" + "\n")
                                    writefile.write("." + "\t" + "O" + "\n")
                                    write_found_special_character(special_character_found, special_character, writefile)

                                elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-PER" + "\n")
                                    writefile.write("," + "\t" + "O" + "\n")

                                else:
                                    writefile.write(word + "\t" + "I-PER" + "\n")
                                    write_found_apostrophe(apostrophe_found, char_after, writefile)
                                    write_found_special_character(special_character_found, special_character, writefile)
                                    punctuation_appeared_person = False
                                    comma_appeared_person = False
                                    continue
                                
                                
                        
                        previous_was_person = False
                        punctuation_appeared_person = False
                        comma_appeared_person = False
                            
                    # If capitalized letter, previous word ends with punctuation (e.g. Gl. Byvej) or previous was an address                    
                    elif previous_was_location:
                        if word[0].isupper():
                        
                            if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:
                                # If the word has an ending punctuation of a sentence 
                                if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-LOC" + "\n")
                                    writefile.write("." + "\t" + "O" + "\n")
                                    write_found_special_character(special_character_found, special_character, writefile)

                                elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-LOC" + "\n")
                                    writefile.write("," + "\t" + "O" + "\n")

                                else:
                                    writefile.write(word + "\t" + "I-LOC" + "\n")
                                    write_found_apostrophe(apostrophe_found, char_after, writefile)
                                    write_found_special_character(special_character_found, special_character, writefile)

                        previous_was_location = False
                        punctuation_appeared_location = False
                        comma_appeared_location = False
                    
                    # If capitalized start letter, previous was a word ending with a punctuation, or previous was a city (unsure whether this is necessary)
                    elif previous_was_city:
                        if word[0].isupper():
                            if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:
                                
                                # If the word has an ending punctuation of a sentence
                                if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-LOC" + "\n")
                                    writefile.write("." + "\t" + "O" + "\n")
                                    write_found_special_character(special_character_found, special_character, writefile)

                                elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-LOC" + "\n")
                                    writefile.write("," + "\t" + "O" + "\n")

                                else:
                                    writefile.write(word + "\t" + "I-LOC" + "\n")
                                    write_found_apostrophe(apostrophe_found, char_after, writefile)
                                    write_found_special_character(special_character_found, special_character, writefile)

                        previous_was_city = False
                        punctuation_appeared_city = False
                        comma_appeared_city = False

                    # If capitalized start letter, previous word ended with a punctuation (e.g. St. Lucia), or previous was a country
                    elif previous_was_country:
                        if word[0].isupper():
                            if word not in adresse_map and word not in bynavn_map and word not in landenavne_map and word not in drengenavne_map and word not in pigenavne_map:
                                
                                # If the word has an ending punctuation of a sentence
                                if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip('\n') + "\t" + "I-GEO" + "\n")
                                    writefile.write("." + "\t" + "O" + "\n")
                                    write_found_special_character(special_character_found, special_character, writefile)

                                elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                    writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "I-GEO" + "\n")
                                    writefile.write("," + "\t" + "O" + "\n")

                                else:
                                    writefile.write(word + "\t" + "I-GEO" + "\n")
                                    write_found_apostrophe(apostrophe_found, char_after, writefile)
                                    write_found_special_character(special_character_found, special_character, writefile)

                        previous_was_country = False
                        punctuation_appeared_country = False
                        comma_appeared_country = False
                    
                    else:
                        previous_was_person = False
                        previous_was_location = False
                        previous_was_city = False
                        previous_was_country = False          

                        # If the word is a recognized name
                        # The word is trimmed from comma or punctuation
                        temp_word = word
                        if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            temp_word = word.translate(str.maketrans('', '', string.punctuation))

                        if re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                            temp_word = word.replace(',', '')

                        if temp_word in drengenavne_map or temp_word in pigenavne_map or temp_word.lower() in drengenavne_map or temp_word.lower() in pigenavne_map:
                            previous_was_person = True
                            # If the word has an ending punctuation of a sentenceg
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-PER" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")
                                write_found_special_character(special_character_found, special_character, writefile)
                                previous_was_person = False

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.replace(',', '') + "\t" + "B-PER" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")
                                previous_was_person = False

                            else:
                                writefile.write(word + "\t" + "B-PER" + "\n")
                                write_found_apostrophe(apostrophe_found, char_after, writefile)
                                write_found_special_character(special_character_found, special_character, writefile)
                                punctuation_appeared_person = False
                                comma_appeared_person = False


                        # If the word is a danish address
                        elif temp_word in adresse_map:
                            previous_was_location = True
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-LOC" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")
                                write_found_special_character(special_character_found, special_character, writefile)
                                previous_was_location = False

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.replace(',','') + "\t" + "B-LOC" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")
                                previous_was_location = False

                            else:
                                writefile.write(word + "\t" + "B-LOC" + "\n")
                                write_found_apostrophe(apostrophe_found, char_after, writefile)
                                write_found_special_character(special_character_found, special_character, writefile)

                        # If the word is a danish city
                        elif temp_word in bynavn_map or temp_word.lower() in bynavn_map:
                            previous_was_city = True
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-LOC" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")
                                write_found_special_character(special_character_found, special_character, writefile)
                                previous_was_city = False

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.replace(',', '') + "\t" + "B-LOC" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")
                                previous_was_city = False
                                
                            else:
                                writefile.write(word + "\t" + "B-LOC" + "\n")
                                write_found_apostrophe(apostrophe_found, char_after, writefile)
                                write_found_special_character(special_character_found, special_character, writefile)

                        # If the word is a country
                        elif temp_word in landenavne_map or temp_word.lower() in landenavne_map:
                            previous_was_country = True
                            if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.translate(str.maketrans('', '', string.punctuation)).rstrip("\n") + "\t" + "B-GEO" + "\n")
                                writefile.write("." + "\t" + "O" + "\n")
                                write_found_special_character(special_character_found, special_character, writefile)
                                previous_was_country = False

                            elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
                                writefile.write(word.replace(',', '').rstrip('\n') + "\t" + "B-GEO" + "\n")
                                writefile.write("," + "\t" + "O" + "\n")
                                previous_was_country = False

                            else:
                                writefile.write(word + "\t" + "B-GEO" + "\n")
                                write_found_apostrophe(apostrophe_found, char_after, writefile)
                                write_found_special_character(special_character_found, special_character, writefile)

                        else:
                            # Common word. No need to identify

                            if not check_for_punctuations(word, writefile):
                                writefile.write(word + "\t" + "O" + "\n")
                            write_found_apostrophe(apostrophe_found, char_after, writefile)
                            write_found_special_character(special_character_found, special_character, writefile)



def write_found_apostrophe(is_found, characters, file):
    if is_found:
        if len(characters) != 0:
            file.write("'" + "\t" + "O" + "\n")
            file.write(characters + "\t" + "O" + "\n")
        else:
            file.write("'" + "\t" + "O" + "\n")

def write_found_special_character(is_found, special_character, file):
    if is_found:
        file.write(special_character + "\t" + "O" + "\n")

def is_word_special_character(char_only, file):
    # If char is (
    if char_only is ")":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is (
    if char_only is "(":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is -
    if char_only is "-":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is _
    if char_only is "_":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is "
    if char_only is "\"":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is @
    if char_only is "@":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is '
    if char_only is "'":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is .
    if char_only is ".":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is ,
    if char_only is ",":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is ´
    if char_only is "´":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is ?
    if char_only is "?":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    # If char is !
    if char_only is "!":
        file.write(char_only + "\t" + "O" + "\n")
        return True

    return False


def check_special_characters_named_entities_start(word, file):
    '''Checking for special characters at the start of the word'''

    # If word contains ' at start
    if re.search(r"^\'", word):
        word = re.sub('^\'','', word)
        file.write("'" + "\t" + "O" + "\n")

    # If word contains (
    if re.search(r"^\(", word):
        word = word.replace('(','')
        file.write("(" + "\t" + "O" + "\n")

    # If word contains - at start 
    if re.search(r"^-", word):
        word = word.replace('-','')
        file.write("-" + "\t" + "O" + "\n")

    # If word contains _
    if re.search(r"\_", word):
        word = word.replace('_','')
        file.write("_" + "\t" + "O" + "\n")

    # If word contains " at start 
    if re.search(r"^\"", word):
        word = word.replace('"','')
        file.write("\"" + "\t" + "O" + "\n")

    return word

def check_special_characters_named_entities_end(word):
    '''Checking for special characters at the middle/end of the word'''

    special_character_found = False
    special_character = ""
    # If word contains " at end
    if re.search(r"(?!^\")\"", word):
        special_character_found = True
        special_character = "\""
        word = word.replace('"','')

    # If word contains - at end 
    elif re.search(r"(?!^-)-$", word):
        special_character_found = True
        special_character = "-"
        word = word.replace('-','')

    # If word contains )
    elif re.search(r"\)", word):
        special_character_found = True
        special_character = ")"
        word = word.replace(')','')

    return (word, special_character, special_character_found)

def check_for_apostrophe(word):
    '''Checking for apostrophe in the middle of the word'''
    
    apostrophe_found = False
    char_after = ''
    # If word contains '
    if re.search(r"\'", word):
        apostrophe_found = True
        special_character = "'"
        char_after = re.search(r"\'(\w*)", word).group(1)
        word = re.sub('\'\w*','', word)

    # If word contains '
    elif re.search(r"\´", word):
        apostrophe_found = True
        special_character = "´"
        char_after = re.search(r"\´(\w*)", word).group(1)
        word = re.sub('\'\w*','', word)

    return (word, char_after, apostrophe_found)


def check_for_punctuations(word, file):
    found = False
    # If word contains .
    if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", word):
        found = True
        word = word.rstrip("\n\r")
        file.write(word.translate(str.maketrans('', '', string.punctuation)) + "\t" + "O" + "\n")
        file.write("." + "\t" + "O" + "\n")

    # If word contains ,
    elif re.search(r"\,(?!\d+|\w+|\S|\.|\s[a-z])", word):
        found = True
        word = word.rstrip("\n\r")
        file.write(word.replace(',', '') + "\t" + "O" + "\n")
        file.write("," + "\t" + "O" + "\n")

    # If word contains word,word
    elif re.search(r"(?!\w+),(?=\w+)", word):
        found = True
        words = word.split(",")
        file.write(words[0] + "\t" + "O" + "\n")
        file.write("," + "\t" + "O" + "\n")
        file.write(words[1] + "\t" + "O" + "\n")

    # If word contains word?word
    elif re.search(r"(?!\w+)\?(?=\w+)", word):
        found = True
        words = word.split("?")
        file.write(words[0] + "\t" + "O" + "\n")
        file.write("?" + "\t" + "O" + "\n")
        file.write(words[1] + "\t" + "O" + "\n")
        
    # If word contains ?
    elif re.search(r"\?", word):
        found = True
        file.write("?" + "\t" + "O" + "\n")
        file.write(word.replace('?', '') + "\t" + "O" + "\n")

    # If word contains word!word
    elif re.search(r"(?!\w+)\!(?=\w+)", word):
        found = True
        words = word.split("!")
        file.write(words[0] + "\t" + "O" + "\n")
        file.write("!" + "\t" + "O" + "\n")
        file.write(words[1] + "\t" + "O" + "\n")

    # If word contains !
    elif re.search(r"\!", word):
        found = True
        file.write("!" + "\t" + "O" + "\n")
        file.write(word.replace('!', '') + "\t" + "O" + "\n")

    

    return found
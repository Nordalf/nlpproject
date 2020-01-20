import os
import re

# with open("drdkcorpus.txt", "r+", encoding="utf-8") as file:
#     lines = file.readlines()

# with open("drdkcorpus.txt", "w+", encoding="utf-8") as file:
#     for line in lines:
#         if not re.search(r"http://", line):
#             file.write(line)


# Fjern *: i starten af saetninger : sed -E 's/^\*.|^\:.//g' < drdkcorpus.txt > drdkcorpus1.txt

# \.(?!\d+|\w+|\S|\.|\s[a-z]) En saetning for hver linje

# with open("drdkcorpus1.txt", "r+", encoding="utf-8") as file:
#     lines = file.readlines()

# with open("drdkcorpus2.txt", "w+", encoding="utf-8") as file:
#     for line in lines:
#         if re.search(r"\.(?!\d+|\w+|\S|\.|\s[a-z])", line):
#             file.write(line)

# (?:^\s+\d+|^\s+|^\d+)

with open("drdkcorpus3.txt", "r+", encoding="utf-8") as file:
    lines = file.readlines()

with open("drdkcorpus4.txt", "w+", encoding="utf-8") as file:
    for line in lines:
        if not re.search(r"(?:^\s+\d+|^\s+|^\d+)", line):
            file.write(line)
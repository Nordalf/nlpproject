import os
import re

# with open("drdkcorpus.txt", "r+", encoding="utf-8") as file:
#     lines = file.readlines()

# with open("drdkcorpus.txt", "w+", encoding="utf-8") as file:
#     for line in lines:
#         if not re.search(r"http://", line):
#             file.write(line)


with open("drdkcorpus.txt", "r+", encoding="utf-8") as file:
    lines = file.readlines()

with open("drdkcorpus.txt", "w+", encoding="utf-8") as file:
    for line in lines:
        if not re.search(r"^\*|^\:", line):
            file.write(line.)
        else:
            file.write(line)
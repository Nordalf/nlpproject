# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 14:44:08 2019

@author: alexf
"""


with open("../Version2/body.txt", "rt", encoding='utf-8') as infile:
        text = infile.read().replace('undefined', '')
with open('cleansed_version2.txt', 'wt', encoding='utf-8') as outfile:
    outfile.write(text)
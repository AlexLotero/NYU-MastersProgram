#!/usr/bin/env python3

import subprocess
import string

# run xortool and store the output
key_lengths = subprocess.getoutput('xortool ciphertext.txt')
key_len_lists = key_lengths.split("%")

key_len_only = []
for element in key_len_lists:
    counter = 0

    # remove additional notes of xortool output
    for letter in element:
        if letter in string.ascii_lowercase:
            counter += 1
    
    # remove unecassary characters and store possible key lengths and their likelyhood
    if counter == 0:
        key_len_only.append(element.replace('\n', '').replace(' ', ''))

# create dictionary with lengths as keys and likelihood (as float) as values
key_len_dict = {}
for element in key_len_only:
    foo = element.split(":")
    key_len_dict[foo[0]] = float(foo[1])

# calculate the suspected key length by highest reported likelihood
key_len = max(key_len_dict, key = key_len_dict.get)

# print xortool's calculated key length
print("xortool identified the following key length:", key_len)
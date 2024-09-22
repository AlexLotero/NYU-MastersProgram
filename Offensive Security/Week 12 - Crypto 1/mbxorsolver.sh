#!/usr/bin/env bash

# run xortool noting that the cihpertext is a hex encoded string (-x), the key length is 5 (-l 5), and the most common character is a space (-c " ")
xortool -x -l 5 -c " " ciphertext.txt

# print an empty line for readability
echo

# print that our flag was identified
echo "Flag found: "

# find the flag within our full decrypted text
cat xortool_out/0.out | grep "flag{"
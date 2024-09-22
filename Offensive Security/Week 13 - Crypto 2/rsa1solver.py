#!/usr/bin/env python3

import subprocess

# open ciphertext2 file
file = open("ciphertext.txt", "r")
input = file.read()
file.close()
	
# extract RSA parameters from provided file
input_list = input.split(" = ")
n = int(input_list[1][:-2])
e = int(input_list[2][:-2])
c = int(input_list[3][:-1])

# run RsaCtfTool script providing parameters from provided ciphertext.txt file
result = subprocess.run(["./RsaCtfTool.py", "-n", str(n), "-e", str(e), "--uncipher", str(c)], capture_output=True)

# store and print the script's output
output = result.stderr.decode("utf-8")
print(output)

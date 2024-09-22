#!/usr/bin/env python3

import time
from pwn import *
import secrets

# DEBUG set to provide more output for better understanding of errors
#context.log_level = "DEBUG"

def main():
	start_time = time.time()

	# extract contents of ciphertext.txt file
	file = open("ciphertext.txt", "r")
	input = file.read()
	file.close()

	# create variable to store: the IV and ciphertext, IV/ciphertext as byte strings, and IV/ciphertext as lists of bytes
	input_list = input.split(':')
	iv = input_list[1][1:-11]
	iv_bytes = bytes.fromhex(iv)
	ciphertext = input_list[2][1:-1]
	ciphertext_bytes = bytes.fromhex(ciphertext)
	byte_sz = 2
	iv_bytes_list = [iv[i:i+byte_sz] for i in range(0, len(iv), byte_sz)]
	c_bytes = [iv_bytes] + [ciphertext_bytes[i:i+16] for i in range(0, len(ciphertext_bytes), 16)]
	
	# store a copy of the original ciphertext before edits for reference
	original_c_bytes = c_bytes
	
	# create 16 "random" bytes
	rand = secrets.token_bytes(16)

	# Create remote connection to challenge
	s = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1478)
	# Wait until prompted for NYU netid and send it
	s.recvuntil(b"something like abc123): ")
	s.send(b"aal562\n")
	
	# Wait until prompted for "message" (IV and ciphertext)
	s.recvuntil(b"Gimme a message:")

	# define variables to store: the brute-forced intermediate values - "solved", the entire intermediate value, and the entire decrypted plaintext
	solved = b""
	plaintext_full = []
	intermed_full = b""
	
	# loop to iterate backwards over every element in c_bytes, a list of every 16-byte block in the ciphertext
	for n in range(-2, -len(c_bytes)-1, -1):
		
		# define variables to store the intermediate values and plaintext for each individual block as they are computed
		intermed = b""
		plaintext = b""
		
		# create a variable of the original current ciphertext block before edits
		original_block = original_c_bytes[n]		
		
		# loop to iterate through each byte in the 16-byte block
		for m in range(1, 17):
		
			# iterate through every possible single byte value until the oracle reports a valid padding
			for i in range(0x00, 0xff+1):
			
				# create a 16-byte block made up of random bytes followed by the byte we are brute-forcing and the already solved intermediate value(s)
				new_block = rand[:-m] + bytes([i]) + bytes(z ^ m for z in intermed[::-1])
				
				# replace the original block with our brute-forcing block within the ciphertext
				c_bytes[n] = new_block
				
				# join entire list of blocks into a sigle ciphertext, excluding blocks that have already been solved
				short_c_bytes = c_bytes[:n + 2]
				if (n + 2) == 0:
					new_cipher = b"".join(c_bytes)
				else:
					new_cipher = b"".join(short_c_bytes)
				
				# send iv and ciphertext "message" to oracle
				temp_msg = bytes(iv, "utf-8") + bytes(new_cipher.hex(), "utf-8") + b"\n"
				s.send(temp_msg)
				
				# recieve oracle response, if ciphertext was valid - note the brute-forced value, calculate the intermediate value and plaintext, 
				# and break to the next byte
				out = s.recvuntil(b"Gimme a message:")
				if b"valid message" in out:
					solved += bytes([i])
					intermed += bytes([i ^ m])
					plaintext += bytes([(i ^ m) ^ original_block[-m]])
					break
		
		# append the intermediate values and plaintext for each block once computed
		intermed_full += intermed
		plaintext_full.append(plaintext[::-1])

	# define and populate the entire plaintext by reversing our list of solved blocks
	plaintext_final = b""
	for c in range(len(plaintext_full)-1, -1, -1):
		plaintext_final += plaintext_full[c]
	
	# print the decyrpted plaintext
	print(plaintext_final)
	print(plaintext_final.decode("utf-8"))
	print("Execution Time: --- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
	main()

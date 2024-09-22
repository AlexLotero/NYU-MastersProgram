import time
import libnum
import math

def gcd(x, y):	# source: https://www.geeksforgeeks.org/gcd-in-python/#
	while(y):
		x, y = y, x % y
	return x

def com_mod_atk(c1, c2, e1, e2, n):
	# sources:
	# http://www.math.umd.edu/~immortal/MATH406/lecturenotes/ch8-Additional.pdf
	# https://www.youtube.com/watch?v=uX2z4fZYYkQ
	
	# Greatest Common Devisor, python math library: https://docs.python.org/3/library/math.html
	gcd_out = math.gcd(e1, e2)
	if gcd_out == 1:
		# "Extended Euclidean GCD algorithm, returns (x, y, g) : a * x + b * y = gcd(a, b) = g"
		# sources: https://pypi.org/project/libnum/, https://github.com/hellman/libnum
		α, β, g = libnum.xgcd(e1, e2)
		
		# Since gcd (e1, e2) = 1 we can find α and β with α*e1 + β*e2 = 1 and then we can find P
		# (C1)^α * (C2)^β mod n = (P^e1)^α * (P^e2)^β mod n = P^(α*e1 + β*e2) mod n = P^1 mod n = P mod n
		# sources: http://www.math.umd.edu/~immortal/MATH406/lecturenotes/ch8-Additional.pdf, https://www.youtube.com/watch?v=uX2z4fZYYkQ
		C1_to_α = pow(c1, α, n)
		C2_to_β = pow(c2, β, n)
		decrypt = (C1_to_α * C2_to_β) % n
		return decrypt
	else:
		print ("exponents were not coprime")
		exit()

def main():
	start_time = time.time()
	
	# open ciphertext1 file
	file = open("ciphertext1.txt", "r")
	input1 = file.read()
	file.close()
	
	# open ciphertext2 file
	file = open("ciphertext2.txt", "r")
	input2 = file.read()
	file.close()
	
	# extract RSA parameters from provided files
	input1_list = input1.split(" = ")
	input2_list = input2.split(" = ")
	n = int(input1_list[1][:-2])
	e1 = int(input1_list[2][:-2])
	c1 = int(input1_list[3][:-1])
	e2 = int(input2_list[2][:-2])
	c2 = int(input2_list[3][:-1])
	
	# perform the Common Modulus Attack
	message = com_mod_atk(c1, c2, e1, e2, n)

	# Convert a positive integer to a byte string, byte_len discovered through trial-and_error
	# sources: https://pycryptodome.readthedocs.io/en/latest/src/util/util.html, https://www.adamsmith.haus/python/docs/Crypto.Util.asn1.long_to_bytes
	byte_len = 55
	plaintext = message.to_bytes(byte_len, byteorder='big')
	
	# print the decyphered plaintext
	print(plaintext)

if __name__ == "__main__":
	main()

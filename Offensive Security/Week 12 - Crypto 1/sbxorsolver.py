#!/usr/bin/env python3

import time

#ciphertext = "fff5f8fee2dbebecedaac6ffa9ebfafcc6dfcdcec6aeaba1f8a0faaba0ffaef8fbe4"

def decryptor(cipher_ints, start_time):
    # xor ciphertext with each possible hex byte until string with the 'flag{' format is located and print it
    for i in range(0x00, 0xff):
        decrypted = ''
        for j in cipher_ints:
            decrypted += chr(i^j)
        if "flag{" in decrypted:
            print("Single-byte key: ", i)
            print("Flag decrypted: ", decrypted)
            print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
            exit()

def main():
    start_time = time.time()

    # open provided file to extract ciphertext
    file = open("ciphertext.txt", "r")
    ciphertext = file.read()
    file.close()
    
    # seperate string of ciphertext into list of individual hex bytes
    n = 2
    cipher_bytes = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]

    # convert bytes from string type to integers
    cipher_ints = []
    for m in cipher_bytes:
        cipher_ints.append(int(m, 16))

    # xor ciphertext with each possible hex byte until string with the 'flag{' format is located and print it
    decryptor(cipher_ints, start_time)

if __name__ == "__main__":
    main()
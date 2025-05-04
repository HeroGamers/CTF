import string
import random

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå'

import os 
# change to current dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Rotate each character by the index of the key character
def mult(a, b):
    # Ignore spaces
    if a in string.whitespace:
        return a
    return alphabet[(alphabet.index(a) * alphabet.index(b)) % len(alphabet)]

def caesar_encrypt(key, text):
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += mult(text[i], key)
    return ciphertext

key = 'a'
while (key == 'a'):
	key = random.choice(alphabet)
print(key)

def main():
    # Danish text, flag is in text
    with open('encryption.txt', 'rb') as f:
        text = f.read().decode("utf-8").strip()

    for letter in alphabet:
        print(letter, caesar_encrypt(letter, text))

    # ddc impossible to save caesar

    # with open('flag.txt', 'wb') as f:
    #     f.write(ciphertext.encode("utf-8"))

    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}


if __name__ == '__main__':
    main()

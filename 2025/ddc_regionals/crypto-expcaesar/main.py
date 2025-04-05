import string
import random
import math
import os

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå'

# Rotate each character by the index of the key character
def mult(a, b):
    # Ignore spaces
    if a in string.whitespace:
        return a
    return alphabet[pow(alphabet.index(a), alphabet.index(b), len(alphabet))]

def caesar_encrypt(key, text):
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += mult(text[i], key)
    return ciphertext

def encrypt():
    key = 'a'
    while (math.gcd(alphabet.index(key), len(alphabet) - 1) != 1):
        key = random.choice(alphabet)
    print(key)

    # Danish text, flag is in text
    with open('flag.txt', 'rb') as f:
        text = f.read().decode("utf-8").strip()

    ciphertext = caesar_encrypt(key, text)

    with open('encryption.txt', 'wb') as f:
        f.write(ciphertext.encode("utf-8"))




def decrypt():
    # We must brute force the key
    with open('encryption.txt', 'rb') as f:
        ciphertext = f.read().decode("utf-8").strip()
    
    # Try all possible keys
    for key in alphabet:
        plaintext = caesar_encrypt(key, ciphertext)
        # Check if the plaintext contains the flag format
        if plaintext.startswith("ddc"):
            print(f"Key: {key}")
            print(f"Plaintext: {plaintext}")
            break

    else:
        print("No flag found.")
    # Uncomment the line below to decrypt the ciphertext



def main():
    # Change directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    decrypt()
    # encrypt()

    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}


if __name__ == '__main__':
    main()

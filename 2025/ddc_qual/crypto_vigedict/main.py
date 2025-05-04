import string
import os

# Change dir to current dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå'

# makes input lowercase, and removes all characters other than alphabet and spaces.
def clean_input(text):
    text = text.lower()
    tmp = [c if c in (alphabet + string.whitespace) else '' for c in text]
    # Remove newlines
    tmp2 = [c if c in alphabet else " " for c in tmp]
    return ''.join(tmp2)

def add(a, b):
    # ignore spaces and newlines
    if a in string.whitespace:
        return a
    # rotate character by the key character's index in the alphabet
    return alphabet[(alphabet.index(a) + alphabet.index(b)) % len(alphabet)]

def subtract(a, b):
    # ignore spaces and newlines
    if a in string.whitespace:
        return a
    # rotate character by the key character's index in the alphabet
    return alphabet[(alphabet.index(a) - alphabet.index(b)) % len(alphabet)]

def vigenere_encrypt(key, text):
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += add(text[i], key[i%len(key)])
    return ciphertext

def vignere_decrypt(key, text):
    plaintext = ""
    for i in range(len(text)):
        plaintext += subtract(text[i], key[i%len(key)])
    return plaintext


def encrypt_stuff():
    # Read the key from file
    with open("key.txt", "rb") as f:
        key = f.read().decode("utf-8").strip()

    assert len(key) == 9

    # Danish text, flag is in text
    with open('danish_text.txt', 'rb') as f:
        text = f.read().decode("utf-8")

    text = clean_input(text)
    ciphertext = vigenere_encrypt(key, text)

    with open('encryption.txt', 'wb') as f:
        f.write(ciphertext.encode("utf-8"))

    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}

def decrypt_stuff():
    with open('encryption.txt', 'rb') as f:
        text = f.read().decode("utf-8").strip()

    # Brute force the key (all possible keys are 9 characters long)
    # Until the first 3 characters are "ddc"

    # Read all possible keys (danish_dict)
    with open("danish_dict.txt", "rb") as f:
        keys = f.read().decode("utf-8").strip().split("\n")

    for key in keys:
        if not len(key) == 9:
            continue
        plaintext = vignere_decrypt(key, text)
        if plaintext[:3] == "ddc":
            print(key)
            print(plaintext)
            # strækning
            # ordbogsangreb er farlige
            break

def main():
    #encrypt_stuff()
    decrypt_stuff()


if __name__ == '__main__':
    main()

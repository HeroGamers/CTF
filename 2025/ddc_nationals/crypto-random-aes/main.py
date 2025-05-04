from Crypto.Cipher import AES
import random

import os


# Sample a random 128 bit key by selecting an integer between 0 and 2^128, then converting to bytes
def genkey():
    key_int = random.randrange(0,2^128)
    key_bytes = key_int.to_bytes(16,'little')
    return key_bytes



# Encrypt with AES CTR mode
def encrypt_flag(flag, key):
    aes = AES.new(key, AES.MODE_CTR)
    ct = aes.encrypt(flag)
    return aes.nonce, ct

def decrypt_flag(nonce, ct, key):
    aes = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return aes.decrypt(ct)

def encrypt():
    with open("flag.txt", "rb") as f:
        flag = f.read()

    key = genkey()
    nonce, ct = encrypt_flag(flag, key)

    with open("output.txt", "w") as f:
        f.write(f'iv = {nonce.hex()}\n')
        f.write(f'ct = {ct.hex()}\n')

def decrypt():
    with open("output.txt", "r") as f:
        lines = f.readlines()
        nonce = bytes.fromhex(lines[0].split('=')[1].strip())
        ct = bytes.fromhex(lines[1].split('=')[1].strip())

        while True:
            key = genkey()
            try:
                flag = decrypt_flag(nonce, ct, key)
                print(flag.decode())
                break
            except:
                pass

if __name__ == "__main__":
    # Change to current dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    decrypt()
    # DDC{Oh_oops_writing_too_much_sage_recently}
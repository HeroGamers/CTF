#!/usr/bin/env python3
import itertools
import numpy as np
from pwn import *


def decode_input(encoded_input: bytes):
    def decode_base64(encode_64_input: bytes):
        try:
            block_padded64 = encode_64_input + b'=' * ((4 - len(encode_64_input) % 4) % 4)
            # print(f"[DEBUG] Trying to decode to base64: {block_padded64}")
            try_decoded = base64.b64decode(block_padded64)
            # Check for valid UTF-8 characters
            char_check = try_decoded.decode("utf-8")
            for char in char_check:
                if not (ord('0') <= ord(char) <= ord('9')) and not (ord('a') <= ord(char) <= ord('z')) and not (
                        ord('A') <= ord(char) <= ord('Z')) and not char == '=':
                    raise Exception(f"Invalid character: {char} in {char_check}")
            # print(f"[DEBUG] Successfully decoded to base64: {try_decoded}")
            return try_decoded
        except Exception as e:
            # print(f"[DEBUG] Failed to decode to base64: {e}")
            return b''

    def decode_base32(encode_32_input: bytes):
        try:
            block_uppercase = encode_32_input.upper()
            block_padded = block_uppercase + b'=' * ((8 - len(block_uppercase) % 8) % 8)
            # print(f"[DEBUG] Trying to decode to base32: {block_padded}")
            try_decoded = base64.b32decode(block_padded)
            char_check = try_decoded.decode("utf-8")
            for char in char_check:
                if not (ord('0') <= ord(char) <= ord('9')) and not (ord('a') <= ord(char) <= ord('z')) and not (
                        ord('A') <= ord(char) <= ord('Z')) and not char == '=':
                    raise Exception(f"Invalid character: {char} in {char_check}")
            # print(f"[DEBUG] Successfully decoded to base32: {try_decoded}")
            return try_decoded
        except Exception as e:
            # print(f"[DEBUG] Failed to decode to base32: {e}")
            return b''

    # For reverting
    last_decoded = []
    last_i = []

    i = 0
    current_encoded_input = encoded_input
    while True:
        if not current_encoded_input:
            break
        if current_encoded_input.isdigit():
            break

        # If there is already padding, we strip it as we calculate padding ourselves.
        if b'=' in current_encoded_input:
            current_encoded_input = current_encoded_input[:current_encoded_input.index(b'=')]

        decoded = b""
        current_try_decode = b""

        # print(f"[INFO] NEW LOOP WITH: {current_encoded_input[:100]}")

        while current_encoded_input:
            try_decoded = decode_base64(current_encoded_input[i:i+4+1])
            if try_decoded:
                # Save last state if we need to revert
                last_i.append(i)
                last_decoded.append(len(decoded))

                # Update state
                decoded += try_decoded
                i += 4
            else:
                # Add 4 characters to the current try decode and try again with base32
                try_decoded = decode_base32(current_encoded_input[i:i+8+1])
                if try_decoded:
                    decoded += try_decoded
                else:
                    # Go back to last state and try again with base32
                    success = False
                    while len(last_i) > 0 and not success:
                        # Try to revert and try with base32
                        i = last_i.pop() if last_i else 0
                        decoded = decoded[:(last_decoded.pop() if last_decoded else 0)]

                        # Add 4 characters

                        # Try to decode
                        try_decoded = decode_base32(current_encoded_input[i:i+8+1])
                        if try_decoded:
                            decoded += try_decoded
                            success = True
                    if success:
                        continue
                    print("NO PROGRESS, STOPPING!")
                    exit()
                i += 8

        current_encoded_input = decoded
        i = 0
    return current_encoded_input


LENGTH = 6
letter_set = string.ascii_letters + string.digits
hex_set = "0123456789abcdef"


def PoW_solve(given: str, h: str) -> str:
    for ch in itertools.product(hex_set, repeat=LENGTH):
        ch = ''.join(ch)
        if h == hashlib.md5(f"SE2:{given}:{ch}".encode()).hexdigest():
            return ch


def PoW():
    a = ''.join(random.choice(letter_set) for i in range(20))
    b = ''.join(random.choice(hex_set) for i in range(LENGTH))
    h = hashlib.md5(f"SE2:{a}:{b}".encode()).hexdigest()

    print("======== Proof-of-Work enabled ========")
    print(f"Send me a {LENGTH}-digit hex code (in lowercase) such that:")
    print(f"md5(\"SE2:{a}:\" + \"<{LENGTH}-digit hex code>\") = {h}")

    ans = input("> ")
    if len(ans) != LENGTH:
        print("Length must be 6!")
        exit()

    if h != hashlib.md5(f"SE2:{a}:{ans}".encode()).hexdigest():
        print("Proof-of-Work failed!")
        exit()


solves = 0

r = remote("chal.firebird.sh", 35011, level='debug')

# PoW


print("============================\nPoW\n============================")

question = r.recvuntil(b"> ")
print(question.decode("utf-8"))
md5_stuff = question.split(b"md5(\"SE2:")[1]
a = md5_stuff.split(b":")[0]
length = md5_stuff.split(b"<")[1].split(b"-")[0]
h = md5_stuff.split(b" = ")[1].split(b"\n")[0]
print(f"a: {a}, h: {h}, length: {length}")
ans = PoW_solve(a.decode("utf-8"), h.decode("utf-8"))
r.send(ans.encode("utf-8") + b"\n")


# Stage 1

print("============================\nStage 1\n============================")

question = r.recvuntil(b"Guess the number: ")
encoded_text = question.split(b"\n")[-2]
print(f"Received: {encoded_text[:100]} ...")

# with open("guess_number_stage_1.txt", "w") as f:
#     f.write(encoded_text.decode("utf-8"))

r.send(decode_input(encoded_text) + b"\n")

# Stage 2

print("============================\nStage 2\n============================")

question = r.recvuntil(b"Guess the number: ")
encoded_text = question.split(b"\n")[-2]
print(f"Received: {encoded_text[:100]} ...")

# with open("guess_number_stage_2.txt", "w") as f:
#     f.write(encoded_text.decode("utf-8"))


r.send(decode_input(encoded_text) + b"\n")

# Stage 2+

print("============================\nStage 2+\n============================")

question = r.recvuntil(b"Guess the number: ")
encoded_text = question.split(b"\n")[-2]
print(f"Received: {encoded_text[:100]} ...")


r.send(decode_input(encoded_text) + b"\n")

# Stage 1,2+

print("============================\nStage 1,2+\n============================")

question = r.recvuntil(b"Guess the number: ")
encoded_text = question.split(b"\n")[-2]
print(f"Received: {encoded_text[:100]} ...")


r.send(decode_input(encoded_text) + b"\n")


r.interactive()



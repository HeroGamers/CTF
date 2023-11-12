#!/usr/bin/env python3
import base64
import hashlib
import random
import string
import itertools
import math
import re
import codecs
import binascii


class Logger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def info(self, msg):
        print(f"[INFO] {msg}")

    def debug(self, msg):
        if self.verbose:
            print(f"[DEBUG] {msg}")

    def warning(self, msg):
        print(f"[WARNING] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}")


logger = Logger(verbose=False)

def changeCaseBase64(ct):
    # decode base64
    def dec(n):
        return base64.b64decode(n)

    def dec32(n):
        return base64.b32decode(n)

    # change the casing of a block
    def tryCase(n, i):
        # get i as 4-bit binary number
        b = format(i, '#06b')[2:]
        # declare a variable for each character in chunk
        c1 = n[0]
        c2 = n[1]
        c3 = n[2]
        c4 = n[3]
        # set them to upper if their respective bit is 1
        if b[0] == '1':
            c1 = c1.upper()
        else:
            c1 = c1.lower()
        if b[1] == '1':
            c2 = c2.upper()
        else:
            c2 = c2.lower()
        if b[2] == '1':
            c3 = c3.upper()
        else:
            c3 = c3.lower()
        if b[3] == '1':
            c4 = c4.upper()
        else:
            c4 = c4.lower()
        # return the result
        return c1 + c2 + c3 + c4

    # check if the decoded b64 falls within valid flag-characters
    def isValid(n):
        try:
            # try to decode, if n contains non-ASCII characters, will automatically return false
            b = n.decode("utf-8")
            # interate through decoded n
            for i in b:
                # if decoded n is less than 32 i.e. where pritable characters start, return false
                if not (ord(i) >= ord('0') and ord(i) <= ord('9')) and not (ord(i) >= ord('a') and ord(i) <= ord('z')) and not (ord(i) >= ord('A') and ord(i) <= ord('Z')):
                    return False
            # if n gets here, we can be sure it's a good character and we can return true
            return True
        except:
            return False

    # split the ciphertext into 4 character blocks (aka 3-character chunks in plaintext)
    block_size = 4
    blocks = [ct[i:i + block_size] for i in range(0, len(ct), block_size)]
    # declares plaintext
    pt = ""
    # iterates blocks
    # print(blocks)
    fails = 0
    for i in blocks:
        # base64 block
        # smol_blocks = [i[:4], i[4:]]
        pt_tmp = ""
        # iterates the 16 possible states a block can have (4 characters each either upper- or lower-case)
        for j in range(4*4):
            # define c as a test-case for the state of the block
            # c1 = dec(tryCase(smol_blocks[0], j))
            # c2 = dec(tryCase(smol_blocks[1], j))
            c = dec(tryCase(i, j))
            # check if c is valid
            # if isValid(c1) and isValid(c2):
            if isValid(c):
                # if yes, append decoded chunk to plaintext and continue to the next block
                pt_tmp += c.decode()
                break
        if not pt_tmp:
            fails += 1
            print("No pt! Fails: " + str(fails))
        else:
            print("Was valid")
        pt += pt_tmp

    return pt

base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def decode_input(encoded_input: bytes):
    def decode_base64(encode_64_input: bytes):
        try:
            block_padded64 = encode_64_input + b'=' * ((4 - len(encode_64_input) % 4) % 4)
            logger.debug(f"Trying to decode to base64: {block_padded64}")
            try_decoded = base64.b64decode(block_padded64)
            # Check for valid UTF-8 characters
            char_check = try_decoded.decode("utf-8")
            for i in char_check:
                if not (ord('0') <= ord(i) <= ord('9')) and not (ord('a') <= ord(i) <= ord('z')) and not (
                        ord('A') <= ord(i) <= ord('Z')) and not i == '=':
                    raise Exception(f"Invalid character: {i} in {char_check}")
            logger.debug(f"Successfully decoded to base64: {try_decoded}")
            return try_decoded
        except Exception as e:
            logger.debug(f"Failed to decode to base64: {e}")
            return b''

    def decode_base32(encode_32_input: bytes):
        try:
            block_uppercase = encode_32_input.upper()
            block_padded = block_uppercase + b'=' * ((8 - len(block_uppercase) % 8) % 8)
            logger.debug(f"Trying to decode to base32: {block_padded}")
            try_decoded = base64.b32decode(block_padded)
            char_check = try_decoded.decode("utf-8")
            for i in char_check:
                if not (ord('0') <= ord(i) <= ord('9')) and not (ord('a') <= ord(i) <= ord('z')) and not (
                        ord('A') <= ord(i) <= ord('Z')) and not i == '=':
                    raise Exception(f"Invalid character: {i} in {char_check}")
            logger.debug(f"Successfully decoded to base32: {try_decoded}")
            return try_decoded
        except Exception as e:
            logger.debug(f"Failed to decode to base32: {e}")
            return b''

    # For reverting
    last_try_decode = []
    last_encoded_input = []
    last_decoded = []

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
        itr = 0
        last_count = 0

        logger.info(f"NEW LOOP WITH: {current_encoded_input[:100]}")

        while current_encoded_input:
            current_try_decode += current_encoded_input[:4]
            current_encoded_input = current_encoded_input[4:]

            logger.debug(f"Current decoded (end): {decoded[-100:]}")
            logger.debug(f"Current encoded (begin): {current_encoded_input[:100]}")

            if len(decoded) != last_count:
                last_count = len(decoded)
                itr = 0
            else:
                itr += 1
                if itr > 5:
                    success = False
                    while len(last_decoded) > 0 and not success:
                        # Try to revert and try with base32
                        logger.warning(f"=========== NO PROGRESS, REVERTING! ({len(last_decoded)}) ============")
                        current_try_decode = last_try_decode.pop() if last_try_decode else b""
                        current_encoded_input = last_encoded_input.pop() if last_encoded_input else b""
                        decoded = last_decoded.pop() if last_decoded else b""

                        # Add 4 characters
                        current_try_decode += current_encoded_input[:4]
                        current_encoded_input = current_encoded_input[4:]

                        logger.debug(f"Current decoded (end): {decoded[-100:]}")
                        logger.debug(f"Current encoded (begin): {current_encoded_input[:100]}")

                        # Try to decode
                        try_decoded = decode_base32(current_try_decode)
                        if try_decoded:
                            decoded += try_decoded
                            current_try_decode = b""
                            itr = 0
                            success = True
                        # else:
                        #     # Try with base64
                        #     try_decoded = decode_base64(current_try_decode)
                        #     if try_decoded:
                        #         decoded += try_decoded
                        #         current_try_decode = b""
                        #         itr = 0
                        #         success = True
                    if success:
                        continue
                    logger.error("NO PROGRESS, STOPPING!")
                    exit()

            try_decoded = decode_base64(current_try_decode)
            if try_decoded:
                # Save last state if we need to revert
                last_decoded.append(decoded)
                last_try_decode.append(current_try_decode)
                last_encoded_input.append(current_encoded_input)

                # Update state
                decoded += try_decoded
                current_try_decode = b""
            else:
                # Add 4 characters to the current try decode and try again with base32
                current_try_decode += current_encoded_input[:4]
                current_encoded_input = current_encoded_input[4:]

                logger.debug(f"Current decoded (end): {decoded[-100:]}")
                logger.debug(f"Current encoded (begin): {current_encoded_input[:100]}")

                try_decoded = decode_base32(current_try_decode)
                if try_decoded:
                    decoded += try_decoded
                    current_try_decode = b""

        current_encoded_input = decoded
    return current_encoded_input


# with open("guess_number_stage_1.txt", "r") as f:
# with open("guess_number_stage_2.txt", "r") as f:
# with open("guess_number_stage_2_plus.txt", "r") as f:
with open("guess_number_stage_1_2_plus.txt", "r") as f:
    base64_code = f.read()
    print(base64_code[:100])

    decoded = decode_input(base64_code.encode("utf-8"))

    print(decoded)

exit()

# answer 6066427
# with open("guess_number_stage_1_2_plus.txt", "r") as f:
#     base64_code = f.read()
#     print(base64_code[:200])
#
#     # If there is already padding we strip it as we calculate padding ourselves.
#     if '=' in base64_code:
#         base64_code = base64_code[:base64_code.index('=')]
#     base64_code = base64_code + '=' * ((4 - len(base64_code) % 4) % 4)
#
#     base64_code = changeCaseBase64(base64_code)
#     print(base64_code[:200])
#     base64_code = base64_code + '=' * ((4 - len(base64_code) % 4) % 4)


    # base64_code = base64_code.upper()
    # print(base64_code[:200])

    # remove invalid base32
    # base64_code = re.sub(r'[^A-Z2-7=]', '', base64_code)
    # print(base64_code[:200])

    # If there is already padding we strip it as we calculate padding ourselves.
    # if '=' in base64_code:
    #     base64_code = base64_code[:base64_code.index('=')]
    # base64_code = base64_code + '=' * ((4 - len(base64_code) % 4) % 4)

    # Try with custom alphabets
    # new_base64 = base64_code
    # base64_alphabet_new = base64_alphabet
    # while True:
    #     # print("Trying new alphabet: " + base64_alphabet_new + "...")
    #     # translate new_base64 using alphabet
    #     # print("Before: " + new_base64[:200])
    #     new_base64 = new_base64.translate(str.maketrans(base64_alphabet, base64_alphabet_new))
    #     # print("After: " + new_base64[:200])
    #     try:
    #         base64_decoded = base64.b64decode(base64_code)
    #         # print(base64_decoded[:200])
    #         new_base64 = base64_decoded.decode("utf-8")
    #         print("Decode didn't fail with alphabet: " + base64_alphabet_new)
    #         if "6066427" in new_base64:
    #             print("CORRECT ALPHABET: " + base64_alphabet_new)
    #             break
    #     except Exception as e:
    #         # print("Wrong, try new alphabet - error: " + str(e))
    #         new_base64 = base64_code
    #         # get a random base64 alphabet
    #         base64_alphabet_new = ''.join(random.sample(base64_alphabet, len(base64_alphabet)))


    # rot13
    # base64_code = codecs.decode(base64_code, 'rot-13')
    # print(base64_code[:100])

    # other shifts
    # for shift in range(1, 26):
    #     decrypted_text = ""
    #
    #     for char in base64_code:
    #         if char.isalpha():
    #             is_upper = char.isupper()
    #             char = char.lower()
    #             char_code = ord(char) - shift
    #             if char_code < ord('a'):
    #                 char_code += 26
    #             char = chr(char_code)
    #             if is_upper:
    #                 char = char.upper()
    #         decrypted_text += char
    #
    #     # print(decrypted_text[:100])
    #
    #     decrypted_text_padded = decrypted_text + '=' * ((4 - len(decrypted_text) % 4) % 4)
    #     # print(base64_padded[:100])
    #     base64_decoded = base64.b64decode(decrypted_text_padded)
    #     # base64_decoded = base58.b58decode(base64_code)
    #     print(base64_decoded[:100])

    # if uppercase, make lowercase, and vice-versa
    # base64_code_new = ""
    # for i in range(len(base64_code)):
    #     if base64_code[i].isupper():
    #         base64_code_new += base64_code[i].lower()
    #     elif base64_code[i].islower():
    #         base64_code_new += base64_code[i].upper()
    #     else:
    #         base64_code_new += base64_code[i]
    # base64_code = base64_code_new
    # print(base64_code[:100])

    # reverse
    # base64_code = base64_code[::-1]
    # print(base64_code[:100])

    # base64_padded = base64_upper + '=' * ((4 - len(base64_upper) % 4) % 4)
    # base64_code = base64_code + '=' * ((4 - len(base64_code) % 4) % 4)
    # base64_code = base64_code + '=' * ((8 - len(base64_code) % 8) % 8)
    # print(base64_padded[:100])
    # base64_decoded = base64.b64decode(base64_code)
    # base64_decoded = base64.b32decode(base64_code)
    # base64_decoded = base58.b58decode(base64_code)
    # print(base64_decoded[:100])
    # print(str(base64_decoded[:100]))

    # hex_code = re.sub(b'([a-fA-F0-9][a-fA-F0-9])', b'', base64_decoded)
    # print(hex_code[:100])



    # with open("guess_number_hex.txt", "w") as r:
    #     r.write(str(base64_decoded))

    # # use regex to only keep valid HEX characters
    # hex_code = re.findall(r'(\\x[a-fA-F0-9][a-fA-F0-9])', str(base64_decoded))
    # # hex_code = re.findall(r'(\\x[3-7][a-fA-F0-9])', str(base64_decoded))
    # # hex_code = re.sub(b'[^a-fA-F0-9]', b'', base64_decoded)
    # hex_code_join = ''.join(hex_code)
    # print(hex_code_join)
    #
    # # bytes_hex = bytes(hex_code_join, "utf-8")
    # # print(bytes_hex)
    # # print(bytes_hex.replace(b'\\\\', b'\\'))
    #
    # hexcode_no_x = hex_code_join.replace("\\x", "")
    # converted = ""
    #
    # print(hexcode_no_x)
    #
    # for i in range(len(hexcode_no_x)):
    #     if i % 2 != 0:
    #         converted += hexcode_no_x[i]
    #         continue
    #     if hexcode_no_x[i] == '0':
    #         converted += '3'
    #     elif hexcode_no_x[i] == '1':
    #         converted += '4'
    #     elif hexcode_no_x[i] == '8':
    #         converted += '5'
    #     elif hexcode_no_x[i] == '9':
    #         converted += '6'
    #     elif hexcode_no_x[i] == 'a':
    #         converted += '7'
    #     elif hexcode_no_x[i] == 'b':
    #         converted += '3'
    #     elif hexcode_no_x[i] == 'c':
    #         converted += '4'
    #     elif hexcode_no_x[i] == 'd':
    #         converted += '5'
    #     elif hexcode_no_x[i] == 'e':
    #         converted += '6'
    #     elif hexcode_no_x[i] == 'f':
    #         converted += '7'
    #     else:
    #         print("ERROR!!!!! " + hexcode_no_x[i])
    #
    # print(converted)
    #
    # # convert to bytes
    # hex_bytes = binascii.unhexlify(converted)
    # print(hex_bytes)
    #
    # # remove everything that's not base64 characters
    # base64_code_converted = re.sub(b'[^a-zA-Z0-9+/]', b'', hex_bytes)
    #
    # print(base64_code_converted.decode("utf-8"))
    #
    # # decode base64
    # base64_decoded = base64.b64decode(base64_code_converted + b'=' * ((4 - len(base64_code_converted) % 4) % 4))
    # print(base64_decoded)


# exit()
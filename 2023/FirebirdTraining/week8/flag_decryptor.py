import hashlib
import random
from z3 import *


def encrypt_flag(flag, key):
    key = hashlib.md5(key.encode()).hexdigest().encode()
    message = (flag.encode() + b'|' + key)
    enc1 = chr(random.randrange(0xff)).encode()
    for i in range(len(message)):
        enc1 += (((message[i] + key[i % len(key)] + enc1[i]) % 0xff)).to_bytes(1, 'little')
    enc2 = list(enc1)
    for i in range(len(enc2)):
        enc2[i] = enc2[(i - 1) % len(enc2)] ^ enc2[i]
    return bytes(enc2).hex()


def decrypt_flag(encrypted_flag: bytes):
    # Create Z3 solver
    solver = Solver()

    # Define the stuff as BitVec variables
    RANDOM_BYTES = 1
    message = [BitVec(f'message_{i}', 16) for i in range(len(encrypted_flag) - RANDOM_BYTES)]
    enc1 = [BitVec(f'enc1_{i}', 16) for i in range(len(encrypted_flag))]
    enc2 = [BitVecVal(encrypted_flag[i], 16) for i in range(len(encrypted_flag))]

    # Add constraints for reversing XOR operation
    solver.add(enc1[0] == (enc1[-1] ^ enc2[0]))
    for i in range(1, len(enc2)):
        solver.add(enc1[i] == (enc2[i - 1] ^ enc2[i]))

    # Add constraints for reversing addition operation
    key = message[-32:]
    for i in range(RANDOM_BYTES, len(enc1)):
        solver.add(enc1[i] == ((message[i - RANDOM_BYTES] + key[(i - RANDOM_BYTES) % 32] + enc1[i - RANDOM_BYTES]) % 0xff))

    # Add flag constraints
    solver.add(message[0] == ord('f'))
    solver.add(message[1] == ord('l'))
    solver.add(message[2] == ord('a'))
    solver.add(message[3] == ord('g'))
    solver.add(message[4] == ord('{'))

    # Add message constraints for bytes in range 0-256
    for i in range(len(message)):
        solver.add(message[i] >= 0)
        solver.add(message[i] <= 256)

    # Check if the constraints are satisfiable
    if solver.check() == sat:
        model = solver.model()
        message_chars = [model[message[i]].as_long() for i in range(len(message))]
        decrypted_message = bytes(message_chars).decode()
        print("Decrypted message:", decrypted_message)
    else:
        print("Failed to decrypt the flag")


def encrypt_decrypt_flag(flag, key):
    """
Ciphertext is enc2 in hex
enc2[i] is the result of XORing enc1[i-1] (with wraparound) and enc1[i]
so we can get enc1[i] by XORing enc1[i-1] and enc2[i]
enc1[i] is the result of adding message[i], key[i % len(key)], and enc1[i-1] (or end1[i-2] if rand gave us two bytes)
but key can also be found from the last 32 chars of the message: message[:-32]
    """
    key = hashlib.md5(key.encode()).hexdigest().encode()[:5]
    message = (flag.encode() + b'|' + key)
    print(f"{message=}")
    print(f"{len(message)=}")
    enc1 = [random.randrange(0xff)] + [0] * (len(message))
    key = message[-len(key):]
    for i in range(1, len(enc1)):
        enc1[i] = ((message[i - 1] + key[(i - 1) % len(key)] + enc1[i - 1]) % 0xff)
    print(f"{enc1=}")
    enc2 = list(enc1)
    for i in range(len(enc2)):
        enc2[i] = enc2[(i - 1) % len(enc2)] ^ enc2[i]

    print("\nLet's try reversing!")
    print(f"{bytes(enc1)=}")
    print(f"{bytes(enc2)=}")
    # enc1=b'\xc3\xa2_o\x12\x08\xa5qn\xd7'
    # bytes(enc2)=b'\x14\xb6\xe9\x86\x94\x9c9H&\xf1'
    enc1_rev = [0] * len(enc1)
    enc1_rev[0] = enc1[-1] ^ enc2[0]
    for i in range(1, len(enc1)):
        enc1_rev[i] = enc2[i - 1] ^ enc2[i]
    print(f"{bytes(enc1_rev)=}")

    return bytes(enc2).hex()


def main():
    # for i in range(20):
    #     randchar = chr(random.randrange(0xff))
    #     print(f"{randchar=} {len(randchar)=} {ord(randchar)=} {hex(ord(randchar))=} {randchar.encode()=} {len(randchar.encode())=} {randchar.encode()[0]=}")
    # return
    encrypted_flag_hex = "ce1ebc8451d4e8e1918df3ef5f40fcad8b334d06e4a91a524bf2726bc6d27404d7bebad7036c68a5cc32a3a3371adb530f06ddaa77010ed64a4dd4d2743592df238ec92962d79a8f3f21a44b15dfe827b39a24a1810ef3673fcc426bff06669f0df5"
    # encrypt_decrypt_flag("hi", "key")
    # return
    # encrypted_flag_hex = encrypt_flag("flag{hi}", "key")
    print(f"{encrypted_flag_hex=}")

    # Convert the encrypted flag to bytes
    encrypted_flag = bytes.fromhex(encrypted_flag_hex)

    print(f"{len(encrypted_flag)=}")

    decrypt_flag(encrypted_flag)


if __name__ == "__main__":
    main()

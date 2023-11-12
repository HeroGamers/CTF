import hashlib
import random
from z3 import *

flag = 'flag{hi}'
key = 'hi'


def encrypt_flag(flag, key):
    key = hashlib.md5(key.encode()).hexdigest().encode()
    print(f"{key=}")
    message = (flag.encode() + b'|' + key)
    print(f"{message=}")
    print(f"{len(message)=}")
    enc1 = chr(random.randrange(0xff)).encode()
    print(f"random {enc1=}")
    print(f"random {len(enc1)=}")
    for i in range(len(message)):
        enc1 += (((message[i] + key[i % len(key)] + enc1[i]) % 0xff)).to_bytes(1, 'little')
    print(f"{enc1=}")
    print(f"{len(enc1)=}")
    enc2 = list(enc1)
    for i in range(len(enc2)):
        enc2[i] = enc2[(i - 1) % len(enc2)] ^ enc2[i]
    print(f"{bytes(enc2)=}")
    return bytes(enc2).hex()


def decrypt_flag(encrypted_flag):
    enc2 = bytearray.fromhex(encrypted_flag)
    enc1 = bytearray(enc2)

    key_len = 32  # MD5 hash length in bytes
    key = [BitVec(f'key_{i}', 8) for i in range(key_len)]
    message = [BitVec(f'message_{i}', 8) for i in range(len(enc2) - key_len)]

    # Constraints for key and message bytes
    for i in range(key_len):
        enc1[i] = ((message[i] + key[i % key_len] + enc1[i]) % 0xff)
        enc2[i] = enc1[i]

    for i in range(key_len, len(enc2)):
        enc1[i] = ((message[i - key_len] + key[(i - key_len) % key_len] + enc1[i]) % 0xff)
        enc2[i] = enc1[i]

    # Create a solver instance
    solver = Solver()

    # Add constraints to the solver
    for i in range(len(enc2)):
        solver.add(enc2[i] == enc1[i])

    # Check if the solver is satisfiable
    if solver.check() == sat:
        model = solver.model()
        # Extract key and message bytes from the model
        found_key = bytes([model[key[i]].as_long() for i in range(key_len)])
        found_message = bytes([model[message[i - key_len]].as_long() for i in range(key_len, len(enc2))])
        found_flag = found_message.split(b'|')[0].decode()
        return found_flag, found_key.hex()
    else:
        return None, None


def reverse_flag(encrypted_flag):
    enc2 = bytes.fromhex(encrypted_flag)
    s = Solver()
    flag = [BitVec(f'flag_{i}', 8) for i in range(len(enc2))]
    s.add([flag[i] ^ flag[(i - 1) % len(flag)] == enc2[i] for i in range(len(enc2))])
    if s.check() == sat:
        m = s.model()
        original_flag = ''.join(chr(m[flag[i]].as_long()) for i in range(len(enc2)))
        flag_index = original_flag.find('|')
        return original_flag[:flag_index]
    else:
        return None

def decrypt_flag_2(encrypted_flag):
    # Convert hexadecimal input to bytes
    encrypted_bytes = bytes.fromhex(encrypted_flag)

    # Create Z3 variables for decryption
    dec1 = [BitVec(f'dec1_{i}', 8) for i in range(len(encrypted_bytes))]
    dec2 = [BitVec(f'dec2_{i}', 8) for i in range(len(encrypted_bytes))]

    # Reverse the second encryption pass (XOR operation)
    for i in range(len(encrypted_bytes)):
        if i > 0:
            dec1[i] = dec2[i] ^ dec2[i - 1]
        else:
            dec1[i] = dec2[i]

    # Reverse the first encryption pass (addition and modulo operation)
    for i in range(len(encrypted_bytes)):
        dec1[i] = (dec1[i] - dec2[i] - dec1[i - 1]) % 0xff

    # Create constraints to match the known format of the input flag
    constraints = [
        dec1[-1] == ord('|'),
        # Add more constraints if you have additional knowledge about the flag format
    ]

    # Use Z3 to solve the constraints
    solver = Solver()
    solver.add(constraints)
    if solver.check() == sat:
        model = solver.model()
        # Reconstruct the flag from the model
        decrypted_flag = ''.join(chr(model[dec1[i]].as_long()) for i in range(len(encrypted_bytes)))
        return decrypted_flag
    else:
        return None

def main():
    encrypted_flag = encrypt_flag(flag, key)
    print(encrypted_flag)

    man_decrypt_flag(encrypted_flag, key)

    # encrypted_flag = "ce1ebc8451d4e8e1918df3ef5f40fcad8b334d06e4a91a524bf2726bc6d27404d7bebad7036c68a5cc32a3a3371adb530f06ddaa77010ed64a4dd4d2743592df238ec92962d79a8f3f21a44b15dfe827b39a24a1810ef3673fcc426bff06669f0df5"
    # found_flag = decrypt_flag_2(encrypted_flag)
    # if found_flag:
    #     print(f"Found Flag: {found_flag}")
    # else:
    #     print("Decryption failed.")
    # print(reverse_flag(encrypted_flag))



if __name__ == "__main__":
    main()

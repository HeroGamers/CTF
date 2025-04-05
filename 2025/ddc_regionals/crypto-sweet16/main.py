import os
import random

# Constants for the 16-bit PRESENT cipher
ROUNDS = 31  # Number of rounds
S_BOX = [
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
]  # S-box
S_BOX_INV = [
    0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD,
    0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA
]  # Inverse S-box
P4 = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]  # Permutation table
P4_INV = [P4.index(i) for i in range(16)]  # Inverse permutation

def sbox_substitution(value, sbox):
    """Apply the S-box substitution using the given S-box."""
    result = 0
    for i in range(4):
        nibble = (value >> (i * 4)) & 0xF
        result |= sbox[nibble] << (i * 4)
    return result

def permutation(value, perm_table):
    """Apply a bit permutation using the given table."""
    permuted = 0
    for i in range(16):
        if value & (1 << i):
            permuted |= (1 << perm_table[i])
    return permuted

def generate_round_keys(key):
    """Generate round keys from the 80-bit master key."""
    round_keys = []
    for i in range(ROUNDS):
        # Extract the round key (16 most significant bits)
        round_keys.append((key >> 64) & 0xFFFF)
        # Rotate key left by 19 bits
        key = ((key << 19) & (2**80 - 1)) | (key >> (80 - 19))
        # Apply S-box to the leftmost 4 bits of the rotated key
        key = ((S_BOX[(key >> 76) & 0xF] << 76) | (key & (2**76 - 1)))
        # XOR the round counter into bits 15 to 11 of the key
        key ^= i << 15
    return round_keys

def present_encrypt(plaintext, round_keys):
    """Encrypt a 16-bit plaintext using the 16-bit PRESENT cipher with 80-bit key."""
    state = plaintext
    for i in range(ROUNDS - 1):
        state ^= round_keys[i]  # Add round key
        state = sbox_substitution(state, S_BOX)  # S-box substitution
        state = permutation(state, P4)  # Permutation
    # Final round: only XOR with the last round key
    state ^= round_keys[-1]
    return state

def present_decrypt(ciphertext, round_keys):
    """Decrypt a 16-bit ciphertext using the 16-bit PRESENT cipher with 80-bit key."""
    state = ciphertext
    # Inverse of final round
    state ^= round_keys[-1]
    for i in range(ROUNDS - 2, -1, -1):
        state = permutation(state, P4_INV)  # Inverse permutation
        state = sbox_substitution(state, S_BOX_INV)  # Inverse S-box substitution
        state ^= round_keys[i]  # Remove round key
    return state

def cbc_encrypt(plaintext_blocks, key, iv):
    round_keys = generate_round_keys(int.from_bytes(key))
    ciphertext_blocks = []
    previous_block = iv

    for block in plaintext_blocks:
        block ^= previous_block  # XOR with the previous ciphertext block
        encrypted_block = present_encrypt(block, round_keys)
        ciphertext_blocks.append(encrypted_block)
        previous_block = encrypted_block  # Update for the next block

    return ciphertext_blocks

def cbc_decrypt(ciphertext_blocks, key, iv):
    round_keys = generate_round_keys(int.from_bytes(key))
    plaintext_blocks = []
    previous_block = iv

    for block in ciphertext_blocks:
        decrypted_block = present_decrypt(block, round_keys)
        plaintext_block = decrypted_block ^ previous_block  # XOR with previous ciphertext
        plaintext_blocks.append(plaintext_block)
        previous_block = block  # Update for the next block

    return plaintext_blocks

def pad_data(data, block_size=2):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad_data(padded_data):
    pad_len = padded_data[-1]
    return padded_data[:-pad_len]

def bytes_to_blocks(data):
    blocks = []
    for i in range(0, len(data), 2):
        blocks.append(int.from_bytes(data[i:i+2], byteorder='big'))
    return blocks

def blocks_to_bytes(blocks):
    return b''.join(block.to_bytes(2, byteorder='big') for block in blocks)

if __name__ == "__main__":
    key = random.randbytes(10)
    round_keys = generate_round_keys(int.from_bytes(key, byteorder='big'))
    
    ciphertexts = list()
    for plaintext in range(0, 624):
        c = present_encrypt(plaintext, round_keys)
        ciphertexts += [c]
    print(*ciphertexts, sep=" ")

    flag = open("flag.txt", "r")
    plaintext = flag.readline().strip().encode("utf-8")  # Example plaintext
    assert(len(plaintext) == 46)

    iv = int.from_bytes(os.urandom(2), byteorder='big')  # 16-bit IV
    # Padding and block conversion
    padded_plaintext = pad_data(plaintext)
    plaintext_blocks = bytes_to_blocks(padded_plaintext)
    ciphertext_blocks = [iv] + cbc_encrypt(plaintext_blocks, key, iv)
    ciphertext = blocks_to_bytes(ciphertext_blocks)
    print(f"Ciphertext: {ciphertext.hex()}")
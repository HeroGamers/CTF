from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate a random key (same key for both encryption and MAC)
key = get_random_bytes(16)
iv = get_random_bytes(16)

def pad_data(data, block_size=16):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad_data(padded_data):
    pad_len = padded_data[-1]
    return padded_data[:-pad_len]

# Function to perform AES-CBC encryption
def aes_cbc_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad_data(plaintext)
    return cipher.encrypt(padded_plaintext)

# Function to compute CBC-MAC (last block of CBC encryption)
def cbc_mac(key, message, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad_data(message)
    ciphertext = cipher.encrypt(padded_message)
    return ciphertext[-16:]

# Function to perform AES-GCM encryption
def aes_ctr_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    return cipher.encrypt(plaintext)

# Function to perform AES-GCM decryption
def aes_ctr_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    return cipher.decrypt(ciphertext)

# Function to verify the integrity of the message
def decrypt_and_verify_cbc_mac(key, ciphertext, iv):
    # Decrypt the ciphertext to get the combined data (y || CBC-MAC(y))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad_data(cipher.decrypt(ciphertext))
    
    # Separate the data (x) and the MAC (last block)
    x_decrypted = decrypted_data[:-16]  # All except last 16 bytes
    received_mac = decrypted_data[-16:]  # Last 16 bytes (the MAC)
    
    # Compute the MAC for the received data (x)
    computed_mac = cbc_mac(key, x_decrypted, iv)
    
    # Check if the computed MAC matches the received MAC
    if (computed_mac == received_mac):
        return x_decrypted
    else:
        return b''

# Data (x) to be encrypted
x = b"!Attack at dawn tomorrow!"

# Encrypt under CTR with 96-bit IV, as within GCM.
ciphertext = aes_ctr_encrypt(key, x, iv[0:12])

# Step 1: Compute the MAC (same key, same IV as CBC encryption)
mac = cbc_mac(key, ciphertext, iv)

# Step 2: Re-encrypt the data with the appended MAC.
# Final data: AES-CBC(y = AES-CTR(x) || CBC-MAC(y))
ciphertext = iv + aes_cbc_encrypt(key, ciphertext + mac, iv)

# Output the steps
print("Original Data (x):", x)
print("Ciphertext:", ciphertext.hex())

print("Give me the modified ciphertext, quick!")
ciphertext = bytes.fromhex(input())

# Step 3: Verify the integrity of the received ciphertext
print("\nVerifying the integrity of the received ciphertext...")
iv = ciphertext[:16]
combined = decrypt_and_verify_cbc_mac(key, ciphertext[16:], iv)
plaintext = aes_ctr_decrypt(key, combined, iv[0:12])

if (plaintext == b"!Attack at dusk tomorrow!"):
    flag = open("flag.txt", "r")
    print(flag.readline())
else:
    print(f"MAC verification failed! {plaintext}")
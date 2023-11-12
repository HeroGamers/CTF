import random
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
import base64
from pwn import xor
import itertools
from tqdm import tqdm
from sympy.ntheory.modular import solve_congruence
import libnum


def xor_bruteforce(a):
    for length in tqdm(range(1, len(a) + 1)):
        for combination in itertools.combinations(range(len(a)), length):
            candidate = bytearray(a)
            for index in combination:
                candidate[index] ^= a[index]
            yield candidate


def cipher(k, m, n):
    return (k * m) % n


def encrypt(flag, key, n):
    k, m = bytes_to_long(key), bytes_to_long(flag)
    assert m < n and len(flag) == len(key)

    c1 = long_to_bytes(cipher(k, m, n))
    c2 = xor(key, flag)

    print("c1 =", base64.b64encode(c1).decode())
    print("c2 =", base64.b64encode(c2).decode())
    print("n =", n)

    return c1, c2, n


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def pollards_rho(n):
    x = random.randint(1, n-1)
    y = x
    c = random.randint(1, n-1)
    d = 1

    while d == 1:
        x = (x**2 + c) % n
        y = (y**2 + c) % n
        y = (y**2 + c) % n
        d = GCD(abs(x-y), n)

    return d


def decrypt_mod(c1, c2, n):
    # Decode base64-encoded c1
    c = bytes_to_long(c1)

    gcd, x, y = extended_gcd(n, c)
    assert gcd == 1

    print(f"gcd: {gcd}")

    # Calculate k_times_m_mod_n_c1
    k_times_m_mod_n_c1 = (x * n + y * c) % (n * c)
    print(f"k_times_m_mod_n_c1: {k_times_m_mod_n_c1}")

    # Find the modular multiplicative inverse of c modulo n
    try:
        c_inv = inverse(c, n)
    except ValueError:
        print("Error: Modular multiplicative inverse does not exist. Cannot recover the flag.")
        exit()

    print(f"c_inv: {c_inv}")

    # Get k * m
    km = (c_inv * k_times_m_mod_n_c1) % (n * c)

    print(f"km: {km}")

    # Factorize km using Pollard's Rho or another suitable factorization algorithm
    k = pollards_rho(km)
    m = km // k

    print(f"k: {k}")
    print(f"m: {m}")

    # Calculate the original key
    key = long_to_bytes(k)

    print(f"key: {key}")

    # Reverse the XOR operation to get the original flag
    flag = xor(c2, key)

    print(f"flag: {flag}")
    print(f"flag: {flag.decode()}")



def brute_xor(c2):
    for candidate in xor_bruteforce(c2):
        if b"flag{" in candidate:
            print(candidate)

def solve_flag_using_crt(n, c1, c2):
    # Convert c1 to long
    c1 = bytes_to_long(c1)

    # Calculate partial_key and partial_key_end
    partial_key = bytes_to_long(xor(c2[:5], b'flag{'))
    partial_key_end = bytes_to_long(xor(c2[-1:], b'}'))

    # Calculate modular equations
    mod_eq1 = (c1 * partial_key) % n
    mod_eq2 = (c1 * partial_key_end) % n

    # Define the congruences and moduli
    rem = [mod_eq1, mod_eq2]
    mod = [n, n]

    # Solve the congruences using the Chinese Remainder Theorem
    res = libnum.solve_crt(rem, mod)

    print(res)

    print(long_to_bytes(res))

def decrypt2(c1, c2, n):
    # Calculate the GCD of c2 and n to find the common factor
    common_factor = GCD(bytes_to_long(c2), n)

    print(common_factor)

    # Check if the common factor is non-trivial
    if 1 < common_factor < n:
        # Calculate the original message m
        m = (bytes_to_long(c1) * inverse(common_factor, n)) % n

        # Check if the decrypted message is a valid flag format
        decrypted_message = long_to_bytes(m)
        if decrypted_message.startswith(b'flag{') and decrypted_message.endswith(b'}'):
            print("Decrypted message:", decrypted_message.decode())
            return

    print("Decryption failed.")

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def crt(c1, c2, n):
    m1 = bytes_to_long(c1)
    m2 = bytes_to_long(c2)

    q1 = n
    q2 = len(c2)

    inv_q1 = modinv(q1, q2)
    inv_q2 = modinv(q2, q1)

    x = (m1 * q2 * inv_q2 + m2 * q1 * inv_q1) % (n * q1)
    return x


def decrypt(c1, c2, n):
    # We can get the following information from the XOR'd ciphertext
    key_length = len(c2)
    key_start = xor(b'flag{', c2[:5])
    key_end = xor(b'}', c2[-1:])

    # Brute force the remaining key bytes
    for middle_key_bytes in tqdm(itertools.product(range(256), repeat=key_length - 6)):
        key = key_start + bytes(middle_key_bytes) + key_end

        # Use CRT to calculate the original message
        m = crt(c1, xor(key, c2), n)

        # Check if the decrypted message is a valid flag format
        decrypted_message = long_to_bytes(m)
        if decrypted_message.startswith(b'flag{') and decrypted_message.endswith(b'}'):
            print("Decrypted message:", decrypted_message.decode())
            break

def xor_brute2(c1, c2, n):
    c1 = bytes_to_long(c1)
    key_start = xor(b'flag{', c2[:5])
    key_end = xor(b'}', c2[-1:])

    # Brute-force XOR key
    prefix = b"flag{"
    key_length = len(c2) - len(prefix) - len(b"}")
    for i in range(2 ** (key_length * 8)):
        candidate_key = key_start + long_to_bytes(i, key_length) + key_end
        decrypted_message = xor(c2, candidate_key)

        print(candidate_key)
        print(decrypted_message)

        # Check if decrypted message starts with "flag{"
        if decrypted_message.startswith(prefix):
            # Decrypt c1 using the found key
            key_inverse = inverse(c1, n)
            m = (key_inverse * bytes_to_long(candidate_key)) % n
            print("Decrypted Flag:", long_to_bytes(m).decode())
            break


def decrypt_again(c1, c2, n):
    c1 = bytes_to_long(c1)

    gcd, x, y = egcd(c1, n)
    assert gcd == 1

    mod_inv = x % n

    print(mod_inv)

    k = (mod_inv * c1) % n

    print(k)
    print(long_to_bytes(k))


if __name__ == "__main__":
    # Provided values
    with open("output.txt", "r") as output:
        c1 = base64.b64decode(output.readline().split(" = ")[1].strip())
        c2 = base64.b64decode(output.readline().split(" = ")[1].strip())
        n = int(output.readline().split(" = ")[1].strip())

        print(f"c1: {c1}")
        print(f"c2: {c2}")
        print(f"n: {n}")

    # c1, c2, n = encrypt(b"flag{", b"\x99\x93\x9e\x98\x84", n)

    # decrypt_mod(c1, c2, n)
    # decrypt(c1, c2, n)
    # decrypt2(c1, c2, n)
    # xor_brute2(c1, c2, n)
    # yet_another_decrypt(c1, c2, n)
    decrypt_again(c1, c2, n)
    # solve_flag_using_crt(n, c1, c2)
    # brute_xor(c1, c2)




    # create array of size key_len
    # possible_combinations = []
    # for i in range(key_len):
    #     if i < len(known_prefix):
    #         possible_combinations.append([known_prefix[i]])
    #     elif i >= key_len - len(known_suffix):
    #         possible_combinations.append([known_suffix[i - (key_len - len(known_suffix))]])
    #     else:
    #         possible_combinations.append([])
    #
    # for i in range(len(known_prefix), key_len-len(known_suffix)):
    #     for j in range(len(alphabet)):
    #         xord = xor(alphabet[j], c2[i])
    #         if b'\x70' < xord < b'\xa0':
    #             possible_combinations[i].append(alphabet[j])
    #
    # print(possible_combinations)

import itertools
import math

import sympy
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
import base64
from pwn import xor
from tqdm import tqdm
import numpy as np

NUM_THREADS = 3
alphabet = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
known_prefix = b'flag{'
known_suffix = b'}'


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


def brute_force_flag(n, c1, c2):
    c1 = bytes_to_long(c1)
    c1_inv = inverse(c1, n)

    # Precompute the xor of the known flag prefix and suffix with the corresponding c2 bytes
    key_len = len(c2)
    fill_length = key_len - len(known_prefix) - len(known_suffix)

    total_combinations = len(alphabet) ** fill_length

    for i in tqdm(itertools.product(alphabet, repeat=fill_length), total=total_combinations):
        flag_candidate = known_prefix + bytes(i) + known_suffix

        if check_result(n, c1_inv, c2, flag_candidate):
            return flag_candidate


def check_result(n, c1_inv, c2, flag_candidate):
    key = xor(c2, flag_candidate)
    k = bytes_to_long(key)
    m = bytes_to_long(flag_candidate)

    # Use Chinese Remainder Theorem (CRT) for modulo operation
    c1_inv_k_m = pow(c1_inv * k * m, 1, n)  # (k * m * c1_inv) % n == 1

    # Check if c1_inv_k_m ≡ 1 (mod n)
    return c1_inv_k_m == 1


def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def find_k_and_m(c1, c2, n):
    for k in range(n):
        # Calculate m using the formula: m = (k + c2) * modular_inverse(1 - k, n) % n
        m = (k + c2) * modular_inverse(1 - k, n) % n
        if (k * m) % n == c1:
            return k, m
    raise ValueError("No valid k and m found")


def solve_ciphertexts(c1, c2, n):
    # Solve for k using extended Euclidean algorithm
    a = 2 * (1 - 2 * c1 % n)
    b = n
    x, y, gcd = extended_gcd(a, b)
    k = (x * (2 * c1 + c2)) % n

    # Solve for m using first equation
    m = (c1 * pow(k, -1, n)) % n

    return k, m


def extended_gcd(a, b):
    if a == 0:
        return (0, 1, b)
    else:
        x, y, gcd = extended_gcd(b % a, a)
        return (y - (b // a) * x, x, gcd)


def find_k_and_m_2(c1, c2, n):
    # Calculate k using c2 = (k + m) mod n
    k = (c2 - c1) % n

    # Calculate modular multiplicative inverse of k
    k_inverse = inverse(k, n)

    # Calculate m using c1 = (k * m) mod n
    m = (c1 * k_inverse) % n

    return k, m


def solve_equation(c1, c2, n):
    discriminant = c2 ** 2 - 4 * (c1 - n)

    if discriminant < 0:
        return None, None  # No real solutions

    sqrt_discriminant = math.isqrt(discriminant)

    print(sqrt_discriminant)

    x1 = (c2 + sqrt_discriminant) // 2
    x2 = (c2 - sqrt_discriminant) // 2

    print(x1)
    print(x2)

    return x1, x2


def discriminant(a, b, c):
    return b ** 2 - 4 * a * c


def find_possible_values(c1, c2, n):
    x = 0
    a = 1
    b = -c2
    c = c1 - x

    # Calculate discriminant: (c2 - x) ** 2 - 4 * (c1 - x)
    D = discriminant(a, b, c)
    print("Discriminant:", D)
    # Check if the discriminant is a perfect square modulo n
    if D >= 0 and math.isqrt(D) ** 2 == D:
        # Calculate square root of D modulo n
        D_sqrt = math.isqrt(D) % n

        # Calculate m values using the quadratic formula
        m1 = ((-b + D_sqrt) / (2 * a)) % n
        m2 = ((-b - D_sqrt) / (2 * a)) % n

        # Calculate corresponding k values
        k1 = (c2 - m1) % n
        k2 = (c2 - m2) % n

        # Print the solutions
        print("Possible solutions for m and k:")
        print("(m1, k1):", m1, k1)
        print("(m2, k2):", m2, k2)
    else:
        print("No solutions found.")


def solve_quadratic(a, b, c, n):
    D = (b ** 2 - 4 * a * c) % n
    if GCD(2 * a, n) != 1:
        raise ValueError("Inverse of 2a mod n does not exist")

    sqrt_discriminant = pow(D, (n + 1) // 4, n)  # Compute modular square root
    inv_2a = inverse(2 * a, n)

    m1 = (sqrt_discriminant - b) * inv_2a % n
    m2 = (-sqrt_discriminant - b) * inv_2a % n

    return m1, m2


def find_possible_values_2(c1, c2, n):
    a = 1
    b = -c2
    c = c1

    m1, m2 = solve_quadratic(a, b, c, n)
    # m1, m2 = solve_quadratic_2(c1, c2, n)

    k1 = (c2 - m1) % n
    k2 = (c2 - m2) % n

    print("Possible solutions for m and k:")
    print("(m1, k1):", m1, k1)
    print("(m2, k2):", m2, k2)
    # (m1, k1): 9223336818122948608 9223336818122948607
    # (m2, k2): 9223336818122948607 9223336818122948608
    return m1, k1


def solve_quadratic_2(c1, c2, n):
    # Compute modular inverse of 2
    two_inverse = inverse(2, n)
    # Compute discriminant
    D = (c2 * c2 - 4 * c1) % n

    # Check if D is a quadratic residue modulo n
    if pow(D, (n - 1) // 2, n) != 1:
        return None, None  # No solutions if D is not a quadratic residue

    # Compute square root of D modulo n (using a modular square root algorithm)
    x = pow(D, (n + 1) // 4, n)

    # Compute solutions using the quadratic formula
    m1 = ((-c2 + x) * two_inverse) % n
    m2 = ((-c2 - x) * two_inverse) % n

    return m1, m2


def solve_quadratic_congruence(c1, c2, n):
    # Iterate through possible values of a until a quadratic residue is found
    a = 2  # Start with 2, as 1 is a quadratic residue for all n
    while True:
        # Calculate the discriminant
        D = discriminant(c2, c1, a) % n

        # Check if the discriminant is a quadratic residue modulo n
        # legendre_sym = legendre_symbol(discriminant, n)
        legendre_sym = sympy.legendre_symbol(D, n)
        if legendre_sym == 1:
            # If it's a quadratic residue, find square roots modulo n
            # sqrt_discriminant = sympy.modsqrt(discriminant, n)
            sqrt_discriminant = inverse(D, n) ** ((n + 1) // 4) % n

            # Calculate two possible solutions for m
            m1 = (c2 + sqrt_discriminant) * pow(2, -1, n) % n
            m2 = (c2 - sqrt_discriminant) * pow(2, -1, n) % n

            print(f"Possible solutions for m: {m1}, {m2}")

            return m1, m2
        else:
            # Increment a and continue searching
            a += 1

def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)

def modular_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        raise ValueError("No modular square root exists")
    elif a == 0:
        return 0
    elif p == 2:
        return a

    for i in range(1, p):
        if legendre_symbol(i ** 2 - a, p) == p - 1:
            return pow(i, (p + 1) // 2, p)

def solve_quadratic_congruence_2(c1, c2, n):
    d = ((c2 ** 2) // 4 - c1) % n
    try:
        x1 = modular_sqrt(d, n)
        sol1 = (c2 // 2 + x1) % n
        sol2 = (c2 // 2 - x1) % n

        print(f"x1: {x1}")
        print(f"Possible solutions for m: {sol1}, {sol2}")

        return sol1, sol2
    except ValueError:
        return None


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

def solve_crt(c1, c2, n):
    n1, n2 = n, 2
    m1, m2 = c1, c2

    # Finding modular multiplicative inverse
    inv_n1_mod_n2 = pow(n1, -1, n2)
    inv_n2_mod_n1 = pow(n2, -1, n1)

    # Calculating combined solution
    x = (m1 * n2 * inv_n1_mod_n2 + m2 * n1 * inv_n2_mod_n1) % (n1 * n2)

    # Calculating m and k from x
    m = x % n
    k = x // n

    print(f"Possible solutions for m and k: ({m}, {k})")

    return k, m

def try_own_encrypt(n):
    print(f"\n\n\nDOING OWN ENCRYPTION WITH FAKEKEY")
    fakeflag = b'flag{' + b'\xff' * 2 + b'}'
    # fakeflag = b'\xff' * 4
    # # make bytearray of 1's with lengt fakeflag
    bytarr = bytearray(b'\xff\xff' * (len(fakeflag) // 2))
    bytarr[3] = 0b11101111
    bytarr[2] = 0b10111111
    print(bin(bytes_to_long(bytarr)))
    fakekey = xor(fakeflag, bytarr)
    print(f"fakekey: {fakekey}")
    print(f"fakeflag: {fakeflag}")
    print(bytes_to_long(fakeflag))
    print(bytes_to_long(fakekey))

    #
    # # key = flag ^ 11101 (and some random 0's?)
    # # encryptkey = key ^ flag = flag ^ 11101 ^ flag = 11101
    # # encryptkey ^ key = 11101 ^ key = 11101 ^ flag ^ 11101 = flag
    #
    # fakekey_rev = xor(fakekey, bytearray(b'\x11' * len(fakeflag)))
    # print(f"fakekey_rev: {fakekey_rev}")
    #

    c1, c2, n = encrypt(fakeflag, fakekey, n)
    print(f"c1_unencrypted: {c1}")
    print(f"c2_unencrypted: {c2}")
    print(f"n: {n}")

    # fakekey_rev2 = xor(c2, fakekey)
    # print(f"fakekey_rev2: {fakekey_rev2}")

    print(c2.hex())

    c = bytes_to_long(c1)
    print(f"c: {c}")
    c2_long = bytes_to_long(c2)
    print(f"c2_long: {c2_long}")

    key_long = bytes_to_long(fakekey)
    flag_long = bytes_to_long(fakeflag)
    print(f"key_long {key_long.bit_length()}: {key_long}")
    print(f"flag_long {flag_long.bit_length()}: {flag_long}")

    cipher_long = (key_long * flag_long) % n
    print(f"cipher_long: {cipher_long}")

    xor_long = key_long ^ flag_long  # k ^ m
    print(f"xor_long: {xor_long}")

    xor_arithmetic = (key_long + flag_long)  # (k + m) % n
    print(f"xor_arithmetic: {xor_arithmetic}")

    xor_arithmetic2 = key_long + flag_long - 2 * (key_long & flag_long)  # k + m - 2 * (k & m)
    print(f"xor_arithmetic2: {xor_arithmetic2}")

    # xor_arithmetic3 = (key_long + flag_long) - 2 * (key_long * flag_long // (key_long + flag_long))  # k + m - 2 * (k * m // (k + m))
    # print(f"xor_arithmetic3: {xor_arithmetic3}")

    xor_arithmetic4 = (key_long + flag_long) - 2 * ((key_long + flag_long) // (2 * key_long + 2 * flag_long)) * (
                key_long + flag_long)  # (a + b) - 2 * ((a + b) // (2 * a + 2 * b)) * (a + b)
    print(f"xor_arithmetic4: {xor_arithmetic4}")

    # xor_arithmetic5 = (key_long + flag_long) * (key_long + flag_long) - 4 * key_long * flag_long  # (a + b) * (a + b) - 4 * a * b
    # print(f"xor_arithmetic5: {xor_arithmetic5}")

    xor_arithmetic6 = key_long + flag_long - 2 * (key_long // (flag_long + 1)) * flag_long  # - 2 * (k // (m + 1)) * m
    print(f"xor_arithmetic6: {xor_arithmetic6}")

    xor_carryover = 2 * (key_long & flag_long)
    print(f"xor_carryover: {xor_carryover}")
    print(f"xor_carryover, binary: {bin(xor_carryover)}")
    print(f"key, binary: {bin(key_long)}")

    print("\n\nkey:   " + bin(key_long)[2:].rjust(65, "0"))
    print("flag:  " + bin(flag_long)[2:].rjust(65, "0"))
    print("xor:   " + bin(key_long ^ flag_long)[2:].rjust(65, "0"))
    print("add:   " + bin(key_long + flag_long)[2:].rjust(65, "0"))
    print("and:   " + bin(key_long & flag_long)[2:].rjust(65, "0"))
    print("2and:  " + bin(2 * (key_long & flag_long))[2:].rjust(65, "0"))
    print("-2and: " + bin(key_long + flag_long - 2 * (key_long & flag_long))[2:].rjust(65, "0") + "\n")

    k,m = solve_crt(c, c2_long, n)
    print(f"k: {k}")
    print(f"m: {long_to_bytes(m)}")


    #
    # Verification of the equations
    c1_2 = (k * m) % n
    c2_2 = k ^ m % n  # Bitwise XOR operation

    print("first c1:", c)
    print("Calculated c1:", c1_2)
    print("first c2:", c2_long)
    print("Calculated c2:", c2_2)

    # sol = solve_quadratic_congruence_2(c, c2_long, n)
    #
    # k1 = c2_long - sol[0]
    # k2 = c2_long - sol[1]
    #
    # print(f"k*m % n: {cipher(key_long, flag_long, n)}")
    # print(f"k*m % n: {cipher(k1, sol[0], n)}")
    # print(f"k*m % n: {cipher(k2, sol[1], n)}")
    #
    # print(f"k1: {long_to_bytes(k1)}")
    # print(f"k2: {long_to_bytes(k2)}")
    #
    # print(f"m1: {long_to_bytes(k1 ^ c2_long)}")
    # print(f"m2: {long_to_bytes(k2 ^ c2_long)}")

    # sol = find_possible_values(c, c2_long, n)

    # sol = find_possible_values_2(c, c2_long, n)
    # print(sol)
    #
    # print(f"m: {long_to_bytes(sol[0])}")
    # print(f"k: {long_to_bytes(sol[1])}")
    # print(long_to_bytes(sol[0] ^ sol[1]))
    # print("       " + bin(sol[0])[2:].rjust(65, "0"))
    # print("       " + bin(sol[1])[2:].rjust(65, "0"))
    # print("-2and: " + bin(key_long + flag_long - 2 * (key_long & flag_long))[2:].rjust(65, "0") + "\n")


if __name__ == "__main__":
    # Provided values
    with open("output.txt", "r") as output:
        c1 = base64.b64decode(output.readline().split(" = ")[1].strip())
        c2 = base64.b64decode(output.readline().split(" = ")[1].strip())
        n = int(output.readline().split(" = ")[1].strip())

        print(f"c1: {c1}")
        print(f"c2: {c2}")
        print(bin(bytes_to_long(c2))[2:])
        print(f"n: {n}")

    try_own_encrypt(n)

    # flag = brute_force_flag(n, c1, c2)
    # print(flag)

    # c1 = bytes_to_long(c1)
    # c2 = bytes_to_long(c2)
    #
    # # k, m = solve_ciphertexts(c1, c2, n)
    # k, m = find_k_and_m_2(c1, c2, n)
    # # k, m = find_k_and_m(c1, c2, n)
    # print(f"k: {k}")
    # print(f"m: {m}")
    #
    # key = long_to_bytes(k)
    # print(key)
    # flag = xor(key, long_to_bytes(c2))
    # print(flag)

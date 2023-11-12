from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from sympy.ntheory.modular import crt
import libnum


def enc1(m, key):
    p = key.p
    q = key.q
    e = key.e
    d = pow(e, -1, (p - 1) * (q - 1))

    dp = d % (p - 1)
    dq = d % (q - 1) + getPrime(32)
    qInv = pow(q, -1, p)

    s1 = pow(m, dp, p)
    s2 = pow(m, dq, q)
    h = (qInv * (s1 - s2)) % p
    s = s2 + h * q
    return [s, e, p * q, p, q]


def encrypt(flag=b"flag{hello}"):
    print("[DEBUG] Generating RSA...")
    key = RSA.generate(2048)
    m = bytes_to_long(flag)
    print("[DEBUG] Encrypting...")
    enc = enc1(m, key)
    s = enc[0]
    e = enc[1]
    n = enc[2]
    p = enc[3]

    se_m = (s ** e - m) % n
    print("(s**e - m) % n = ", se_m)  # why?

    print("(e_enc1, n_enc1) = ", (enc[1], enc[2]))

    print("[DEBUG] Generating 3 RSA...")
    c = []
    n_lst = []
    for _ in range(3):
        p = getPrime(1024)
        q = getPrime(1024)
        n = p * q
        e = 3
        assert s ** e > n
        n_lst.append(n)
        c.append(pow(s, e, n))

    print("c = ", c)
    print("n = ", n_lst)
    return se_m, enc[1], enc[2], c, n_lst


def read_encrypt_output():
    with open("output.txt", "r") as output:
        se_m = int(output.readline().split(" = ")[1].strip())
        enc_tuple = output.readline().split(" = ")[1].strip()
        enc_1 = int(enc_tuple.split(",")[0].strip().replace("(", ""))
        enc_2 = int(enc_tuple.split(",")[1].strip().replace(")", ""))
        c = [
            int(x.strip()) for x in
            output.readline().split(" = ")[1].strip().replace("[", "").replace("]", "").split(",")
        ]
        n_lst = [
            int(x.strip()) for x in
            output.readline().split(" = ")[1].strip().replace("[", "").replace("]", "").split(",")
        ]

    return se_m, enc_1, enc_2, c, n_lst


def decrypt_crt(c, n_lst, e=3):
    # Use Chinese Remainder Theorem to solve and get S^e
    sol = crt(m=n_lst, v=c)[0]
    print(f"CRT sol: {sol}")

    # Get S
    s = libnum.nroot(sol, e)
    print(f"CRT s: {s}")

    return s


if __name__ == "__main__":
    # se_m, enc_1, enc_2, c, n_lst = encrypt()
    se_m, enc_1, enc_2, c, n_lst = read_encrypt_output()

    print("(s**e - m) % n = ", se_m)  # why?
    print("(e_enc1, n_enc1) = ", (enc_1, enc_2))
    print("c = ", c)
    print("n = ", n_lst)

    e = enc_1
    n = enc_2

    s = decrypt_crt(c, n_lst, 3)

    m = (s**e - se_m) % n
    print(f"m: {m}")
    print(f"flag: {long_to_bytes(m)}")

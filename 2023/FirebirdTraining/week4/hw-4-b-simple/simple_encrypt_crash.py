from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import base64


def cipher(k, m, n):
    return (k * m) % n


def bruteforce_decrypt(ciphertext, n):
    for k in range(n):  # Try all possible values of k from 0 to n-1
        for m in range(n):  # Try all possible values of m from 0 to n-1
            if cipher(k, m, n) == ciphertext:
                return k, m
    # If no match is found, return None to indicate failure
    return None


def xor(k, m):
    return bytes(a ^ b for a, b in zip(m, k))


def main():
    with open("output.txt", "r") as output:
        c1 = base64.b64decode(output.readline().split(" = ")[1].strip())
        c2 = base64.b64decode(output.readline().split(" = ")[1].strip())
        n = int(output.readline().split(" = ")[1].strip())

        print(f"c1: {c1}")
        print(f"c2: {c2}")
        print(f"n: {n}")

    ciphertext = bytes_to_long(c1)
    print(f"ciphertext: {ciphertext}")
    k, m = bruteforce_decrypt(ciphertext, n)
    print(f"k: {k}, m: {m}")

    print(f"flag: {xor(long_to_bytes(k), c2)}")

    # k, m = bytes_to_long(key), bytes_to_long(flag)
    # n = getPrime(1024)
    # assert m < n and len(flag) == len(key)
    #
    # c1 = long_to_bytes(cipher(k, m, n))
    # c2 = xor(key, flag)
    #
    # print("c1 =", base64.b64encode(c1).decode())
    # print("c2 =", base64.b64encode(c2).decode())
    # print("n =", n)


if __name__ == '__main__':
    main()

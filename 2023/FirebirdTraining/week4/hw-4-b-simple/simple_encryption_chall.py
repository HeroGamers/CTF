from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import base64
from secret import flag, key


def cipher(k, m, n):
    return (k * m) % n


def xor(k, m):
    return bytes(a ^ b for a, b in zip(m, k))


def main():
    k, m = bytes_to_long(key), bytes_to_long(flag)
    n = getPrime(1024)
    assert m < n and len(flag) == len(key)

    c1 = long_to_bytes(cipher(k, m, n))
    c2 = xor(key, flag)

    print("c1 =", base64.b64encode(c1).decode())
    print("c2 =", base64.b64encode(c2).decode())
    print("n =", n)


if __name__ == '__main__':
    main()

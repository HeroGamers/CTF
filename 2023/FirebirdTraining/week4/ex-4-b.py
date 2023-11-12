# Good day! Please find the secret below
# 0x3c55e7cf66f347cd0f200058ce4423f5c9da26d44998d98aff573f0232a95f4c
# The key is generated like so:
# def key_gen():
#     assert len(flag) <= 32
#     p = number.getPrime(255)
#     a = randint(2, p // 2)
#     b = randint(0, len(flag)**2)
#     return a, b, p
#
# The encryption function is as follows:
# def encrypt(m, a, b, p):
#     return (a * m + b) % p


def key_gen():
    assert len(flag) <= 32
    p = number.getPrime(255)
    a = randint(2, p // 2)
    b = randint(0, len(flag)**2)
    return a, b, p

def encrypt(m, a, b, p):
    return (a * m + b) % p
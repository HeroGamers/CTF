def encrypt(G, r, pub_key, message):
    M = message * G  # Encode message as a point on the curve
    k = ZZ.random_element(r)  # Random ephemeral key
    C1 = k * G  # First ciphertext component
    C2 = M + k * pub_key  # Second ciphertext component
    return C1, C2

def decrypt(G, r, priv_key, C1, C2):
    S = priv_key * C1  # Shared secret
    m = discrete_log(C2 - S, G, r, operation='+')  # Recover message point
    return m  # Return the x-coordinate as the plaintext

with open("flag.txt","r") as file:
  flag = file.read()

f = int.from_bytes(flag.encode(), 'big')
assert(f.bit_length() == 255)

print("Give me a prime number: ")
p = int(input())

if p < 2^159 or not(p in Primes()):
	print("wrong prime!")
	exit()

print("Give me a subgroup order: ")
r = int(input())

Fp = GF(p)
a = Fp(0)
b = Fp(7)
E = EllipticCurve(GF(p), [a, b])
n = E.order()

if r < 2^20 or not(r in Primes()) or not(n % r == 0):
	print("wrong factor!")
	exit()

G = (n//r) * E.gens()[0]
sk = ZZ.random_element(r)
P = sk * G

C1,C2 = encrypt(G, r, P, f)

print(G)
print(P)
print(C1)
print(C2)

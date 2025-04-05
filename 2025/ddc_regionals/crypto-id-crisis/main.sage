import random
import hashlib
from bitarray import bitarray

def encrypt_bit(m_bit, a):
	t1 = t2 = random.randint(0, bitsp + bitsq)
	while jacobi(t1, n) != m_bit:
		t1 = random.randint(0, bitsp + bitsq)
	while jacobi(t2, n) != m_bit or t1 == t2:
		t2 = random.randint(0, bitsp + bitsq)

	c1 = (t1 + a * pow(t1, -1, n)) % n
	c2 = (t2 - a * pow(t2, -1, n)) % n
	return (c1, c2)

# Initializes the PKG in Cocks IBE.
bitsp = 1024
bitsq = bitsp - random.randint(0, 64)
bitsp = bitsp - bitsq

# Setup to generate two primes congruent to 3 mod 4
n = p = q = 0
p = next_prime(2^bitsp)
while p % 4 != 3:
	p = next_prime(p)
q = next_prime(2^bitsq)
while p == q or q % 4 != 3:
	q = next_prime(q)
n = p * q
print(n)

# This is an IBE, so here is an identity to extract
id = b"cybermesterskaberne"
a = hashlib.sha256(id).hexdigest()
a_tmp = int(a, 16)

while jacobi(a_tmp, n) != 1:
	a = hashlib.sha256(a_tmp.to_bytes(32)).hexdigest()
	a_tmp = int(a, 16)
a = a_tmp

r = pow(a, (n + 5 - (p+q)) // 8, n)
r2 = (r^2) % n
assert(r2 == a % n or r2 == -a % n)

# Encode the message to bits
with open("flag.txt", "rb") as file:
	msg = file.readline().strip()
x = bitarray()
x.frombytes(msg)
msg_bits = [1 if b else -1 for b in x]

# Encrypt and print the ciphertext tuples
ciphertext = [encrypt_bit(b, a) for b in msg_bits]
for c in ciphertext:
	print(c)


from sage.all import *

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7

Fp = GF(p)
E = EllipticCurve(Fp, [a, b])

def is_valid_x(x):
	rhs = x**3 + a*x + b  # Compute x^3 + ax + b
	return rhs.is_square()  # Check if it's a quadratic residue

def hash_to_curve(E, z):
	c = Fp(2)
	while 1:
		while c.is_square():  
			c += 1

		# Step 1: Compute candidate x values
		t1 = z**2  # t1 = z^2
		t2 = c * t1  # t2 = c * z^2
		x1 = (-b / (1 + t2))  # x1 = -b / (1 + t2)
		x2 = t1 * x1  # x2 = z^2 * x1
		
		# Step 2: Check if x1 is a valid x-coordinate
		x = x1 if is_valid_x(x1) else x2  # Choose the first valid x
		
		# Step 3: Compute y as the square root of x^3 + ax + b
		y = (x**3 + a*x + b).sqrt() # Compute y-coordinate

		if is_valid_x(x):
			return E(x, y)
		else:
			c += 1

F2 = GF(2)
R = PolynomialRing(F2, "x")
x = R.gen()

with open("flag.txt","r") as f:
  flag = f.read()
flag_bits = ''.join(format(ord(i), '08b') for i in flag)
plain = [F2(i) for i in flag_bits]
assert(len(flag_bits) == 360)

poly = R(x**128 + x**7 + x**2 + x + 1)
assert(poly.is_irreducible())
assert(poly.is_primitive())
key = [F2(i) for i in poly.list()]
ini = [F2.random_element() for i in range(0, 128)]
s = lfsr_sequence(key, ini, 360);

cipher = []
for (u, v) in zip(plain, s):
	cipher += [u + v]

d = Fp(0)
for u in ini:
	d = 2*d + int(u)
G = hash_to_curve(E, d)

print(''.join(map(str, cipher)))
print(G)
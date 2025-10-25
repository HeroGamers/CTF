from Crypto.Util.number import inverse, GCD

# Greatest Common Divisor

a=66528
b=52920
print(GCD(a,b)) # 1512

# Modular Arithmetic 1 

# 11≡x mod 6
# 8146798528947≡ y mod  17

x = 11 % 6
y = 8146798528947 % 17
# print(f"({x},{y})")
print(min(x,y)) # 4

# Modular Arithmetic 2 

# the prime p=65537. Calculate 273246787654^65536 mod 65537.

base = 273246787654
exponent = 65536
modulus = 65537
result = pow(base, exponent, modulus)
print(result) # 1

# Modular Inverting 

# What is the inverse element: d=3^(−1) such that 3⋅d≡1 mod  13?
d = inverse(3, 13)
print(d) # 9
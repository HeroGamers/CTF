import math
import os
import json
import base64
from sympy.ntheory.modular import crt
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from pwn import *
import libnum

encrypted_messages = []
modulos = []
e = 17

# Load data from file if available
if os.path.exists("output.json"):
    with open("output.json", "r") as f:
        data = json.load(f)
        encrypted_messages = data["encrypted_messages"]
        modulos = data["modulos"]
else:
    # Gather encrypted messages and modulos
    for _ in range(e):
        r = remote("chal.firebird.sh", 35038)

        r.recvuntil(b"-----BEGIN PUBLIC KEY-----\r\n")
        public_key_base64 = r.recvuntil(b"-----END PUBLIC KEY-----", drop=True).replace(b"\n", b"").replace(b"\r", b"")
        public_key = RSA.import_key(base64.b64decode(public_key_base64))
        current_n = public_key.n
        current_e = public_key.e
        print(f"n: {current_n}")
        print(f"e: {current_e}")
        modulos.append(current_n)

        r.recvuntil(b"The encrypted flag is ")
        encrypted_flag = int(r.recvline().strip())
        print(f"encrypted_flag: {encrypted_flag}")
        encrypted_messages.append(encrypted_flag)

        r.close()

    # Save data to file
    with open("output.json", "w") as f:
        json.dump({"encrypted_messages": encrypted_messages, "modulos": modulos}, f, indent=4)

# Use Chinese Remainder Theorem to solve and get M^e
sol = crt(modulos, encrypted_messages)[0]
print(f"sol: {sol}")

# Get M
m = libnum.nroot(sol, e)
print(f"m: {m}")

# Get flag
flag = long_to_bytes(m)
print(f"flag: {flag}")
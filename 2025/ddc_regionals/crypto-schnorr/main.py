import hashlib
from ecpy.curves     import Curve,Point
from ecpy.keys       import ECPublicKey, ECPrivateKey
from ecpy.formatters import decode_sig, encode_sig, list_formats
from ecpy            import ecrand
from ecpy.ecschnorr  import ECSchnorr
from ecpy.curves     import ECPyException
import secrets
import sys

curve = Curve.get_curve('secp256k1')
pv_key = ECPrivateKey(secrets.randbits(32*8), curve)
print(pv_key)
pb_key = pv_key.get_public_key()

k = secrets.randbits(32*8)

signer = ECSchnorr(hashlib.sha256,"ISO","ITUPLE")

print("Give the first message and I will return a signature: ", end="")
msg = input().strip().encode()
sig = signer.sign_k(msg, pv_key, k)
assert(signer.verify(msg, sig, pb_key))
print(sig)

print("Give the second message and I will return a signature: ", end="")
msg = input().strip().encode()
sig = signer.sign_k(msg, pv_key, k)
assert(signer.verify(msg, sig, pb_key))
print(sig)

print("What is the private key in hex?", end="")
d = input().strip()

if (d == hex(pv_key.d)):
    flag = open("flag.txt", "r")
    print(flag.readline())

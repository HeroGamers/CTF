import os

def decrypt(content):
 def xor(data, key):
  return bytes([a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1))])
 


 encrypted = xor(content, b"6a5265e260f7bed500693b0d21a05cd2")
 print("Decrypted content:", encrypted)
 return encrypted

encrypted = "722576497343565c69730a0456173b560054056650565e3b50023e7d010f5551075140074b"

output = decrypt(bytes.fromhex(encrypted))
# DDC{Ev3n_Cl34r_c0d3_c4n_b3_M4l1c10u5}
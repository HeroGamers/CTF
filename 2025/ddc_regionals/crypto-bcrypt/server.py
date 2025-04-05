#!/usr/bin/python
import bcrypt
import base64

hashes = {}
with open("passwd") as file:
  for line in file:
    fields = line.split(":")
    user = fields[0].strip()
    hash = fields[1].strip()
    hashes[user] = hash

while(1):
  print("server login:", end =" ")
  name = input().strip()
  print("server password:", end =" ")
  password = input().strip()

  bytes = (name + ":" + password).encode('utf-8')
  try:
    if bcrypt.checkpw(bytes, hashes[name].encode("utf-8")):
      flag = open("flag.txt", "r")
      print(flag.readline())
    else:
      print("User is not allowed to login.")
  except:
    print("User is not allowed to login.")	

#!/usr/bin/python
import bcrypt
import secrets

passwd = open("passwd", "w")
length = 20

with open("users.txt", "r") as file:
  for username in file:
    username = username.strip()
    # generate random password
    password = secrets.token_urlsafe(length)
    # converting password to array of bytes 
    bytes = (username + ":" + password).encode('utf-8')
    print(bytes)
    # generating the salt 
    salt = bcrypt.gensalt() 
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    passwd.write(username + ":" + hash.decode("utf-8") + "\n")

file.close()
passwd.close()
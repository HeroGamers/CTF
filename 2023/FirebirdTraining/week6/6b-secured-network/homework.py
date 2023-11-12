#!/usr/bin/env python3
from Crypto.Cipher import AES		
from Crypto.Util.Padding import unpad
import multiprocessing
import os
import socket

flag = os.getenv("FLAG")
# random aes key
key = os.getenv("KEY").encode() if os.getenv("KEY") else os.urandom(16)


def StripBytes(x):
   return x.decode().strip().encode()

class SecureNetwork(object):
    def __init__(self, conn):
        self._conn = conn
        self._auth = False
        self._user = None

    def __del__(self):
        if self._conn:
            self._conn.close()

    @property
    def is_authenticated(self):
        return self._auth

    @property
    def is_authorised(self):
        return self.is_authenticated and self._user == "firebird"

    def response(self, message):
        self._conn.sendall(message)

    def readline(self):
        data = b''
        while True:
            x = self._conn.recv(1)
            if x == b'':
                return None
            elif x == b'\n':
                break
            else:
                data += x
        return data

    def cleanbuffer(self):
        self._conn.setblocking(0)
        self._conn.recv(0x1000)
        self._conn.setblocking(1)

    def decrypt(self, enc, IV):
        enc, IV = bytes.fromhex(enc.decode()), bytes.fromhex(IV.decode())

        print(enc, IV)

        cipher = AES.new(key = key, mode = AES.MODE_CBC, IV = IV)
        return unpad(cipher.decrypt(enc), 16)

    def welcome(self):
        self.response(open('welcome.txt','rb').read())

    def authenticate(self):
        username = password = enc = iv = b''

        self.response(b"Username: ")
        username = self.readline()
        self.response(b"Password: ")
        password = self.readline()

        self.response(b"Encrypted Data (hex): ")
        enc = self.readline()
        self.response(b"IV (hex): ")
        iv = self.readline()

        username, password  = StripBytes(username), StripBytes(password)
        enc,      iv        = StripBytes(enc),      StripBytes(iv)

        e_credentials = self.decrypt(enc, iv)
        credentials = username + b":" + password

        if (e_credentials == credentials):
            self._auth = True
            self._user = username.decode()

        self.cleanbuffer()


def main(conn):
    snw = SecureNetwork(conn)
    snw.welcome()
    try:
        snw.authenticate()
    except Exception:
        pass

    try:
        if snw.is_authenticated:
            snw.response(f"Logged in as {snw._user}.\n".encode())
        if snw.is_authorised:
            snw.response(f"Your flag is {flag}\n".encode())
        if not snw.is_authenticated:
            snw.response(b"Login failed.\n")
    except Exception:
        pass

if __name__ == '__main__':
    enc = "132500ed5fa5ff21b43aca3fb5b572e98abe3be4236830797f1e2eeece92af8fe4e3c78d796fa729979304427641cfd3"
    iv = "a1821b881035c48ca66c8de2a6691cec"

    snw = SecureNetwork(None)
    contents = snw.decrypt(enc.encode(), iv.encode())
    print(contents)


    # Just server stuff. Feel free to run this and test your solve script locally before trying.
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #
    # # print("Listening on 0.0.0.0:3000")
    # sock.bind(('0.0.0.0', 3000))
    # sock.listen(16)
    #
    # # Handle connection
    # ps = []
    # while True:
    #     conn, addr = sock.accept()
    #     ps.append(multiprocessing.Process(target=main, args=(conn,)))
    #     ps[-1].start()
    #     conn.close()
    #     ps = list(filter(lambda p: p.is_alive() or p.join(), ps))

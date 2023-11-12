#!/usr/bin/env python3
import hashlib
import random
import string
import itertools
from pwn import *

LENGTH = 6
letter_set = string.ascii_letters + string.digits
hex_set = "0123456789abcdef"


def PoW_solve(given: str, h: str) -> str:
    for ch in itertools.product(hex_set, repeat=LENGTH):
        ch = ''.join(ch)
        if h == hashlib.md5(f"SE2:{given}:{ch}".encode()).hexdigest():
            return ch


def PoW():
    a = ''.join(random.choice(letter_set) for i in range(20))
    b = ''.join(random.choice(hex_set) for i in range(LENGTH))
    h = hashlib.md5(f"SE2:{a}:{b}".encode()).hexdigest()

    print("======== Proof-of-Work enabled ========")
    print(f"Send me a {LENGTH}-digit hex code (in lowercase) such that:")
    print(f"md5(\"SE2:{a}:\" + \"<{LENGTH}-digit hex code>\") = {h}")
    
    ans = input("> ")
    if len(ans) != LENGTH:
        print("Length must be 6!")
        exit()

    if h != hashlib.md5(f"SE2:{a}:{ans}".encode()).hexdigest():
        print("Proof-of-Work failed!")
        exit()

solves = 0

while True:
    r = remote("chal.firebird.sh", 35009, level='debug')
    for i in range(0, 150):
        if solves == 100:
            r.interactive()
        print("Iteration " + str(i) + " - Solve " + str(solves))
        try:
            math_question = r.recvuntil(b"\r\n", timeout=1)
            if not math_question:
                question = r.recvuntil(b"[y/n]", timeout=1)
                print(question)
                if b"Are you a human?" in question:
                    r.send(b"y\n")
            else:
                if b"If you solve 100" in math_question:
                    continue
                print(math_question)
                math_to_do = math_question.split(b"\r\n")[-2].decode("utf-8")
                print("Math: " + math_to_do)
                # solve = eval(math_to_do)
                #print(solve)
                r.send(str(math_to_do).encode("utf-8") + b"\n")
                solves += 1
        except Exception as e:
            print("Exception: " + str(e))
            break
r.interactive()

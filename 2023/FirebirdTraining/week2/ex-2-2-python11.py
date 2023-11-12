#!/usr/bin/env python3

from pwn import *

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

#!/usr/bin/env python3

from pwn import *


counter_list = []
counter_dict = {b"Scissor": b"R", b"Rock": b"P", b"Paper": b"S"}
current_answer = b"R"

while True:
    r = remote("chal.firebird.sh", 35005, level='debug')
    for i in range(0, 45):
        print(f"Current i = {i} and counter_list = {counter_list}")
        try:
            question = r.recvuntil(b"> ", timeout=5)
            print(str(question))
            if len(counter_list) > i:
                print("In counter list, using counter")
                r.send(counter_list[i] + b"\n")
            elif len(counter_list) == i:
                print("New round!!!!!!!")
                r.send(current_answer + b"\n")
            elif i == 0:
                print("I == 0, sending rock")
                r.send(current_answer + b"\n")
            else:
                print("New counter, appending")
                counter_list.append(current_answer)
                r.send(current_answer + b"\n")
        except EOFError as e:
            print("EOFERROR!!")
            lost = r.recvuntil(b"Try harder!", timeout=5)
            print(lost)
            if lost:
                print("WE LOST!!!!!")
                lost_strings = lost.split(b"\r\n")
                for lost_string in lost_strings:
                    if b"Computer chosen:" in lost_string:
                        current_answer = counter_dict[lost_string.split(b"Computer chosen: ")[1]]
                        counter_list.append(current_answer)
                break
        except Exception as e:
            print("Exception! - " + str(e))
    # if input("Break?") == "y":
    #     break
r.interactive()

## flag{rps_demo_y0u_4r3_RPS_m4s7er_n0w_9lOXEcc5b}
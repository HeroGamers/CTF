#!/usr/bin/env python3
from enum import Enum
import os
import pathlib
# chdir into the Blackjack directory
os.chdir(pathlib.Path(__file__).parent.absolute())
from pwn import *
# to make all variations of 4 chars
import itertools


# ----------------------=[Python Stuff]=---------------------- #

class Mode(Enum):
    DEBUG = 0
    LOCAL = 1
    REMOTE = 2


# ----------------------=[Packing Utils]=---------------------- #

p64 = lambda n: packing.pack(n, 64)
u64 = lambda n: packing.unpack(n, 64)
u32 = lambda n: packing.unpack(n, 32)
uu64 = lambda data: u64(data.ljust(8, b'\x00'))
uu32 = lambda data: u32(data.ljust(4, b'\x00'))

# ---------------------=[Common Settings]=--------------------- #

bin_path = './blackjack'
local_libc_path = './libc.so.6'
remote_url = ''
remote_port = 1337

context.update(arch="amd64", os="linux")
context.log_level = 'error'
context.binary = bin_path

gdb_break_points = [
    ''
]

# ---------------------=[Exploit Functions]=--------------------- #

# Choices
all_possible_4_chars = [bytes(x) for x in itertools.product(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', repeat=4)]
# Current choice
current_choice = -1
def get_choice() -> bytes:
    global current_choice
    current_choice += 1
    return all_possible_4_chars[current_choice]

# -----------------------=[Main Pwn]=-------------------------- #

def do_pwn(io: process | remote) -> None:
    sla = io.sendlineafter
    sa = io.sendafter
    sl = io.sendline
    sd = io.send
    rl = io.recvline
    ru = io.recvuntil

    # rop = ROP(bin_path)
    # elf = ELF(bin_path)
    # libc = ELF(local_libc_path)

    sent_choice = False

    def exploit(sent_choice) -> bool:
        line = rl(timeout=1)
        if line:
            if b"Invalid choice" in line:
                #print("Invalid choice")
                return False
            elif sent_choice:
                print(f"Sent choice {all_possible_4_chars[current_choice]} and got {line}")
                return False
        # Receive until ": ", and get the text before :
        try:
            text = ru(b': ')
        except EOFError:
            #print("EOF")
            return False
        if b"Enter bet" in text:
            #print("Bet")
            sl(b"100")
            return True
        elif b">" in text:
            choice_text = get_choice()
            print(f"Choice: {choice_text}")
            sl(choice_text)
            sent_choice = True
            return True
        elif b"Player bankroll" in text:
            return True
        elif b"Result" in text:
            return True
        elif b"blackjack" in text:
            return True
        else:
            print("Unknown state")
            print(text)
            return False

    status = True
    while status:
        status = exploit(sent_choice)
    # pause()

    # io.interactive()


# --------------------=[End of Exploit]=----------------------- #

def main() -> None:
    while True:
        with process([bin_path]) as io:
            try:
                do_pwn(io)
            except EOFError:
                pass
                #print("EOF")
                # end of file


if __name__ == '__main__':
    main()

# ----------------------------=[EOF]=--------------------------- #

#!/usr/bin/env python3
from enum import Enum
from pwn import *


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

bin_path = './<elf_name>'
local_libc_path = './libc.so.6'
remote_url = ''
remote_port = 1337

context.update(arch="amd64", os="linux")
context.log_level = 'debug'
context.binary = bin_path

gdb_break_points = [
    ''
]


# ------------------------=[Exploit]=-------------------------- #

def initialize_io(mode: Mode) -> process | remote:
    gdbscripts = "handle SIGALRM ignore\n"
    for bp in gdb_break_points:
        if bp:  # is not empty str
            gdbscripts += f"b* {bp}\n"

    # Initialize io based on mode
    match mode:
        case Mode.DEBUG:
            context.terminal = ["tmux", "splitw", "-h"]
            return gdb.debug([bin_path], gdbscripts)
        case Mode.LOCAL:
            return process([bin_path])
        case Mode.REMOTE:
            return remote(remote_url, remote_port)
        case _:
            exit(-1)


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

    def exploit() -> None:
        pass

    exploit()
    # pause()


# --------------------=[End of Exploit]=----------------------- #

def main() -> None:
    io = initialize_io(Mode.DEBUG)
    do_pwn(io)
    io.interactive()


if __name__ == '__main__':
    main()

# ----------------------------=[EOF]=--------------------------- #

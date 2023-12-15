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

# Found via "nmap -v 77.31.48.0/24 -p 6346"
remote_url = '77.31.48.186'
remote_port = 6346

context.update(arch="amd64", os="linux")
# context.log_level = 'debug'

# -----------------------=[Main Pwn]=-------------------------- #

def do_pwn() -> None:
    flag = "################################################"

    while "#" in flag:
        io = remote(remote_url, remote_port)

        rl = io.recvline

        rl()
        flag_part = rl().decode()
        # print(f"{flag_part=}")
        for i in range(len(flag_part)):
            if flag_part[i] != " ":
                flag = flag[:i] + flag_part[i] + flag[i + 1:]

        log.info(f"Flag: {flag}")
        io.close()
    pause()

    # NC3{g0dt_fund3t_nu_3r_du_kl4r_t1l_m3r3_dyn4m1k!}

# --------------------=[End of Exploit]=----------------------- #

def main() -> None:
    do_pwn()

if __name__ == '__main__':
    main()

# ----------------------------=[EOF]=--------------------------- #

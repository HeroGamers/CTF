from pwn import *



if __name__ == '__main__':
    r = remote('chal.hkcert23.pwnable.hk', 28225)

    r.recvuntil(b"Enter math expression:")
    log.info("Ready!")

    r.interactive()

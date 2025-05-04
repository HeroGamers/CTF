from pwn import *

context.update(arch="amd64", os="linux")

info("Do you think cyberlandslaget or cyberlandsholdet is better?")

favorite = input(">> ").encode()
regex = b"[cyberlands(laget|holdet)]"

if set(favorite) - set(regex):
    exit(warn("Yeah, that's not a valid choice 🤷"))

success("Good choice! Let's see if it holds up...")

with process(make_elf(favorite, extract=False), aslr=False, stdin=0) as p:
    p.interactive()
    

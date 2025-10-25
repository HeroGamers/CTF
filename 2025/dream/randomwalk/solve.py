#!/usr/bin/env python3
import os
import random
from Crypto.Util.number import bytes_to_long
from pwn import remote, context

REMOTE = "insert_remote:31337"
LOCAL = "localhost:6843"

FLAG = os.getenv('FLAG', "flag{fakeflag}")

context.update(arch="amd64", os="linux")
context.log_level = 'debug'

mults = 4
# numbers are kept in case you need local hashing (server uses its own numbers).
numbers = [bytes_to_long(os.urandom(3)) for _ in range(mults)]

# on-demand caches (we don't precompute the whole 2**24 table)
hashlookup = {}
rhashlookup = {}
ns = []

def hash24(x):
    x = x & 0xFFFFFF
    x ^= x >> 12
    for num in numbers:
        x = (x * num) & 0xFFFFFF
        x ^= x >> 9
    return x

def hash_lookup(x):
    """Compute/store hash24(x) on demand."""
    if x in hashlookup:
        return hashlookup[x]
    h = hash24(x)
    hashlookup[x] = h
    rhashlookup.setdefault(h, x)
    return h

def inversehash(h):
    return rhashlookup[h]

def perform_walk(io):
    """Send 'walk' and parse returned hashes, return direction: -1, 0, or 1."""
    io.sendline(b'walk')
    io.recvuntil(b'n, m: ')
    n = random.randint(1, 2**24 - 1)
    m = random.randint(1, 2**24 - 1)
    io.sendline(f"{n} {m}".encode())

    io.recvuntil(b'hashes: ')
    hashes = io.recvline().strip().decode()
    n_hash, m_hash = map(int, hashes.split())

    diff = n_hash - m_hash
    if diff == 0:
        return 0
    return 1 if diff > 0 else -1

def do_inverse(io):
    """Ask server for an inverse of a random hash. Return 1 if found, 0 otherwise."""
    io.sendline(b'inverse')
    io.recvuntil(b'hash: ')
    h = random.randint(1, 2**24 - 1)
    io.sendline(str(h).encode())

    response = io.recvline().strip().decode()
    # server prints either an integer, "hash does not exist" or "invalid hash"
    if "invalid hash" in response or "hash does not exist" in response:
        return 0
    try:
        inv = int(response.split()[0])
    except ValueError:
        return 0

    # store parsed ints in caches
    rhashlookup[h] = inv
    hashlookup[inv] = h
    return 1

def solve():
    host, port = LOCAL.split(':')
    io = remote(host, int(port))
    print(f"Connected to {host}:{port}")

    # wait for server to start creating its table and finish
    io.recvuntil(b'creating hashtable please wait a moment')
    io.recvuntil(b'done!', timeout=120)
    print("server ready, starting random walk...")

    randomwalks = 50
    inverses = 25
    position = 0

    while randomwalks > 0:
        print(f"pos={position} | walks_left={randomwalks} | inverses_left={inverses}")
        io.recvuntil(b'[cmd] ')
        direction = perform_walk(io)
        position += direction
        randomwalks -= 1

        if direction == 0 and inverses > 0:
            inverses -= do_inverse(io)

    # keep interactive so you can see final output / flag if the server prints it
    io.interactive()

if __name__ == '__main__':
    solve()

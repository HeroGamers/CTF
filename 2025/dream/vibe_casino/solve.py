#!/usr/bin/env python3
import socket
import re
import sys
import time
import bisect
from typing import List
from pwn import *
import randcrack

HOST = '127.0.0.1'
PORT = 777

# --- Mersenne Twister predictor ---
N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF

class MTPredictor:
    def __init__(self):
        self.mt = [0]*N
        self.index = N
        self.ready = False

    @staticmethod
    def _unshift_right_xor(y: int, shift: int) -> int:
        x = 0
        for i in range(0, 32, shift):
            part = y >> i
            x_part = part ^ (x >> shift)
            mask = (1 << shift) - 1
            x |= (x_part & mask) << i
        return x & 0xFFFFFFFF

    @staticmethod
    def _unshift_left_xor_mask(y: int, shift: int, mask: int) -> int:
        x = 0
        for i in range(0, 32, shift):
            part = y << i
            x_part = part ^ ((x << shift) & mask)
            x |= x_part & (((1 << shift) - 1) << i)
        return (x & 0xFFFFFFFF)

    @classmethod
    def untemper(cls, y: int) -> int:
        y &= 0xFFFFFFFF
        y = cls._unshift_right_xor(y, 18)
        y = cls._unshift_left_xor_mask(y, 15, 0xEFC60000)
        y = cls._unshift_left_xor_mask(y, 7, 0x9D2C5680)
        y = cls._unshift_right_xor(y, 11)
        return y & 0xFFFFFFFF

    def set_state_from_outputs(self, outputs: List[int]):
        assert len(outputs) >= N, 'Need at least 624 outputs'
        self.mt = [self.untemper(y) for y in outputs[:N]]
        self.index = N
        self.ready = True

    def _twist(self):
        for i in range(N):
            y = (self.mt[i] & UPPER_MASK) | (self.mt[(i+1) % N] & LOWER_MASK)
            self.mt[i] = self.mt[(i + M) % N] ^ (y >> 1)
            if y & 1:
                self.mt[i] ^= MATRIX_A
            self.mt[i] &= 0xFFFFFFFF
        self.index = 0

    def next_uint32(self) -> int:
        if not self.ready:
            raise RuntimeError('Predictor not ready')
        if self.index >= N:
            self._twist()
        y = self.mt[self.index]
        # Temper
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)
        self.index += 1
        return y & 0xFFFFFFFF

    def random(self) -> float:
        # Same as CPython: combine two 32-bit outputs to 53-bit float
        a = self.next_uint32() >> 5
        b = self.next_uint32() >> 6
        return (a * 67108864.0 + b) / 9007199254740992.0

# --- socket helpers ---

def recv_until(sock: socket.socket, needle: bytes, timeout=5.0) -> bytes:
    sock.settimeout(timeout)
    data = b''
    while needle not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def send_line(sock: socket.socket, s: str):
    sock.sendall((s + '\n').encode())


NUM_RE = re.compile(rb'Number was (\d+)')
FLAG_RE = re.compile(rb'DREAM\{[^}]+\}')

CUMWEIGHTS = [464, 664, 844, 1000]
SYMS = ['7', 'A', 'B', 'C']

def predict_slot_syms(pred: MTPredictor) -> List[str]:
    out = []
    for _ in range(3):
        r = pred.random() * 1000.0
        j = bisect.bisect(CUMWEIGHTS, r)
        out.append(SYMS[j])
    return out


def main():
    host = HOST
    port = PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    s = socket.create_connection((host, port))

    # Sync to first menu
    recv_until(s, b'Menu:')

    # Gather 624 MT outputs from High-Low
    outputs = []
    for i in range(N):
        send_line(s, '1')  # High-Low
        recv_until(s, b'Enter your bet')
        send_line(s, '1')  # bet 1
        recv_until(s, b'Guess if the number is')
        send_line(s, 'L')  # guess arbitrary
        buf = recv_until(s, b'Remaining plays:')
        m = NUM_RE.search(buf)
        if not m:
            print('Failed to parse number at round', i, file=sys.stderr)
            print(buf.decode(errors='ignore'))
            return 1
        num = int(m.group(1))
        outputs.append(num)
        # Back to menu
        recv_until(s, b'Menu:')

    pred = MTPredictor()
    pred.set_state_from_outputs(outputs)

    # Switch to Slots and snipe only jackpot spins
    coins = None
    target = 1_000_000

    while True:
        send_line(s, '2')  # Slots
        buf = recv_until(s, b'Enter your bet')
        # Determine current balance from last known or query
        # Easier: go to menu 3 to ask balance when needed
        # But we can track: after each spin we know payout text.
        # Ask balance explicitly here to be safe
        # Actually slots prompt includes current coins in message, but server prints only upper bound value.
        # So first fetch Balance if unknown
        if coins is None:
            # Go back to menu and ask balance once
            send_line(s, '1')  # send dummy invalid bet to get error? Better: respond minimal then query balance.
            # Instead, we can cancel: the server doesn't support cancel; Use tracked approach from now on.
            coins = 3000  # initial
        # Predict next spin
        syms = predict_slot_syms(pred)
        jackpot = (syms == ['7','7','7'])
        bet = coins if jackpot else 1
        send_line(s, str(bet))
        # Read result line with symbols
        buf = recv_until(s, b'Slot:')
        buf += recv_until(s, b'You won')
        # Parse payout
        m = re.search(rb'You won (\d+) coins\.', buf)
        payout = int(m.group(1)) if m else 0
        # Update coins: we already paid bet; on win server adds payout
        coins = coins - bet + payout
        # Read until menu returns
        recv_until(s, b'Menu:')
        # Check for flag in any buffered lines
        if FLAG_RE.search(buf):
            print(FLAG_RE.search(buf).group(0).decode())
            break
        if coins >= target:
            # Ask balance to trigger flag print
            send_line(s, '3')
            out = recv_until(s, b'Menu:')
            mflag = FLAG_RE.search(out)
            if mflag:
                print(mflag.group(0).decode())
                break
        # Be nice to the server
        # time.sleep(0.001)

    s.close()

if __name__ == '__main__':
    sys.exit(main() or 0)

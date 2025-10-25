#!/usr/bin/env python3
# adaptive_solve.py
# Adaptive probing solver that uses up to 25 successful `inverse` responses to learn preimages,
# then attempts many (n,m) combinations to bias walk steps positive.
#
# NOT guaranteed, but practical when you can only leak preimages via `inverse`.

import random
import time
from collections import deque, defaultdict
from pwn import remote, context

context.log_level = 'debug'

HOST = "localhost"
PORT = 6843

MASK = (1 << 24) - 1

# Parameters you can tune:
SEED_HASH_START = 27       # smallest hash we can ask inverse for (server requires >26)
SEED_HASH_COUNT = 20       # initial number of target hashes to ask inverse for (<= 25 total allowed)
MAX_INVERSE_SUCCESS = 25   # server allows up to 25 successful inverse answers (tracked)
MAX_TRIES_PER_PAIR = 2     # number of times we'll try a pair before giving up

class AdaptiveSolver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.io = None

        # map: hash_value -> some preimage (int)
        self.h_to_pre = {}
        # map: preimage -> hash_value (immediate)
        self.pre_to_h = {}

        self.used_ns = set()    # server rejects reusing the same n_input
        self.inverse_success_left = MAX_INVERSE_SUCCESS

        # candidate pools
        self.n_candidates = deque()
        self.m_candidates = deque()

        # bookkeeping for attempts
        self.attempts = defaultdict(int)

    def connect(self):
        print("[*] connecting to server...")
        self.io = remote(self.host, self.port)
        # sync with server's start messages
        self.io.recvuntil(b'creating hashtable please wait a moment')
        self.io.recvuntil(b'done!', timeout=120)
        print("[*] server ready")

    def send_inverse(self, h):
        """Ask server for inverse(h). Returns preimage int on success, None on failure."""
        if not (0 <= h < (1 << 24)):
            return None
        if h <= 26:
            return None

        # send inverse command
        self.io.sendline(b'inverse')
        try:
            self.io.recvuntil(b'hash: ')
        except Exception as e:
            print("[!] didn't get 'hash: ' prompt:", e)
            return None

        self.io.sendline(str(h).encode())
        line = self.io.recvline().strip().decode(errors='ignore')
        # server returns either a number, "hash does not exist" or "invalid hash"
        if "hash does not exist" in line or "invalid hash" in line:
            print(f"[inverse {h}] server: {line}")
            return None

        # otherwise parse integer
        try:
            pre = int(line.split()[0])
        except Exception as e:
            print("[!] couldn't parse inverse response:", line, e)
            return None

        # update maps
        if h not in self.h_to_pre:
            self.h_to_pre[h] = pre
            self.pre_to_h[pre] = h
            # candidate pools
            # n candidates must be distinct and not used on server
            if pre not in self.used_ns:
                self.n_candidates.append(pre)
            self.m_candidates.append(pre)
        self.inverse_success_left -= 1
        print(f"[inverse {h}] -> {pre} (inverse_success_left={self.inverse_success_left})")
        return pre

    def seed_initial_inverses(self, start=SEED_HASH_START, count=SEED_HASH_COUNT):
        """Seed the solver with initial inverse queries for a range of hash targets."""
        print(f"[*] seeding inverses for hashes {start}..{start+count-1}")
        for h in range(start, start + count):
            if self.inverse_success_left <= 0:
                break
            # don't re-ask if we already have it
            if h in self.h_to_pre:
                continue
            pre = self.send_inverse(h)
            # if server responded "hash does not exist" it's still counted as failure and inverse_success_left not decremented
            # some server might always return a preimage since table was fully built; handle None gracefully
            if pre is None:
                # give small delay to avoid being too aggressive
                time.sleep(0.05)
                continue
        print(f"[*] seeding done. n_candidates={len(self.n_candidates)} m_candidates={len(self.m_candidates)}")

    def choose_pair(self):
        """Choose next (n_input, m_input) to try.
        Prefer unused n candidates and m candidates we know.
        """
        # pop from left until we find unused n
        while self.n_candidates:
            n = self.n_candidates[0]
            if n in self.used_ns:
                self.n_candidates.popleft()
                continue
            return n, random.choice(list(self.m_candidates)) if self.m_candidates else n
        # if we have no learned n candidates, generate random inputs (last resort)
        n = random.randint(1, MASK)
        m = random.randint(1, MASK)
        return n, m

    def try_walk_once(self, n_input, m_input):
        """Send a single walk(n,m), parse A,B and return direction and values.
        Also tries to harvest inverse on A or B if useful and inverses remain.
        """
        # send walk
        self.io.sendline(b'walk')
        self.io.recvuntil(b'n, m: ')
        self.io.sendline(f"{n_input} {m_input}".encode())

        # read result line: 'hashes: A B' OR maybe 'invalid n and m' etc.
        line = self.io.recvline().strip().decode(errors='ignore')
        if not line:
            print("[!] empty line after walk")
            return None, None, None

        if line.startswith("invalid"):
            print("[!] server returned invalid for walk:", line)
            return None, None, None

        if not line.startswith("hashes:"):
            # server might have printed something else (flag?) — return raw
            print("[*] unexpected server line after walk:", line)
            return None, None, None

        # parse hashes
        try:
            _, rest = line.split(":", 1)
            A_str, B_str = rest.strip().split()[:2]
            A = int(A_str)
            B = int(B_str)
        except Exception as e:
            print("[!] failed to parse hashes line:", line, e)
            return None, None, None

        # compute direction safely
        if A == B:
            # this should trigger exception on server and produce flag soon after
            direction = 0
        else:
            direction = 1 if (A - B) > 0 else -1

        print(f"[walk] n_in={n_input} m_in={m_input} -> A={A} B={B} dir={direction}")

        # Harvest knowledge: if A or B are not known and we still have inverse budget, try to ask inverse for them.
        # Prioritize asking inverse for any printed hash that's small (< some threshold) or that we can use as n target (>=27).
        # Only ask for new hashes and if we have inverse budget left.
        for h in (A, B):
            if h <= 26:
                continue
            if h in self.h_to_pre:
                continue
            # heuristics: prefer A first (because A determines number of iterations), then B
            if self.inverse_success_left > 0:
                self.send_inverse(h)
                # slight pause to avoid any server rate issues
                time.sleep(0.05)

        return direction, A, B

    def run(self):
        """Main loop: attempt to perform randomwalk (50 walks) while trying to bias positive steps."""
        # initial seeds
        self.seed_initial_inverses()

        randomwalks = 50
        position = 0

        print("[*] starting walk loop")
        while randomwalks > 0:
            print(f"[state] pos={position} | walks_left={randomwalks} | inverses_left={self.inverse_success_left}")
            # get a candidate pair
            n_in, m_in = self.choose_pair()
            # ensure distinct ns (server will reject reuse)
            if n_in in self.used_ns:
                # rotate to next
                if n_in in self.n_candidates:
                    self.n_candidates.popleft()
                continue

            pair_key = (n_in, m_in)
            if self.attempts[pair_key] >= MAX_TRIES_PER_PAIR:
                # avoid retrying same pair too much
                # mark n as used-like so we don't select it again
                self.used_ns.add(n_in)
                if n_in in self.n_candidates:
                    self.n_candidates.popleft()
                continue

            # ensure we note this n will be used (if server accepts, it will become used)
            print(f"[*] trying pair n={n_in} m={m_in} (attempt #{self.attempts[pair_key]+1})")
            direction, A, B = self.try_walk_once(n_in, m_in)
            self.attempts[pair_key] += 1

            if direction is None:
                # something went wrong parsing — don't count this n as used, but back off a bit
                time.sleep(0.1)
                continue

            # if server accepted the n, it is now recorded in server's ns; mark as used
            self.used_ns.add(n_in)
            if n_in in self.n_candidates:
                try:
                    self.n_candidates.remove(n_in)
                except Exception:
                    pass

            randomwalks -= 1
            position += direction

            # If direction == 0 then server will likely throw and print flag; we won't see it until next reads.
            if direction == 0:
                print("[*] got direction 0 from walk — server might print flag now. Reading remaining output...")
                # read until EOF or timeout to capture the flag
                try:
                    rest = self.io.recv(timeout=2).decode(errors='ignore')
                    if rest:
                        print("[FLAG OUTPUT]\n", rest)
                except Exception:
                    pass
                return True

            # small cooldown to not blast the server
            time.sleep(0.05)

        # finished walks
        print("[*] finished loop — did not trigger flag in this run")
        return False


def main():
    solver = AdaptiveSolver(HOST, PORT)
    solver.connect()
    success = solver.run()
    if success:
        print("[+] Done — possibly got flag output above.")
    else:
        print("[-] Adaptive probing did not cause server to print the flag. You can try again or increase SEED_HASH_COUNT.")

if __name__ == '__main__':
    main()

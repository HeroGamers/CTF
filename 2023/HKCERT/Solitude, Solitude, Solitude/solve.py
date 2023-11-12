from pwn import *
import random
from z3 import *


class ShamirSecretSharing:
    def __init__(self, p, k=10):
        self.p = p
        self.k = k

        self.secret = random.randrange(0, p)
        # [secret, a1, ..., ak] represents the polynomial "secret + a1*x + ... + ak*x^k"
        self.coefficients = [self.secret] + [random.randrange(0, p) for _ in range(k)]

    # Evaluates coefficients
    def evaluate(self, x: int) -> int:
        print("Evaluating...")
        y = 0
        print(f'{self.coefficients = }')
        for coeff in reversed(self.coefficients):
            print(f'Running for {coeff = }')
            y *= x
            y += coeff
            y %= self.p
            print(f'{y = }')
        return y


def solve_z3(_p=0x7f7df673, _x=1, _y=133, k=10):
    solver = Solver()

    x = BitVecVal(_x, 1024)
    y = BitVecVal(_y, 1024)
    p = BitVecVal(_p, 1024)
    secret = BitVec('secret', 1024)
    coeffs = [BitVec(f'coeff_{i}', 1024) for i in range(k)]

    # We set constraints for x
    solver.add(x % p != 0)

    # We set constraints for y
    solver.add(y ==
               ((((((((((((((((((((((0 * x + coeffs[0]) % p)
                                   * x + coeffs[1]) % p)
                                 * x + coeffs[2]) % p)
                               * x + coeffs[3]) % p)
                             * x + coeffs[4]) % p)
                           * x + coeffs[5]) % p)
                         * x + coeffs[6]) % p)
                       * x + coeffs[7]) % p)
                     * x + coeffs[8]) % p)
                   * x + coeffs[9]) % p)
                 * x + secret) % p)
               )

    # Check if there is a solution
    if solver.check() == sat:
        # Get the model
        model = solver.model()
        print(f'{model = }')
        # Get the value of secret
        secret_value = model[secret].as_long()
        print(f'{secret_value = }')
    else:
        print("No solution!")


def play():
    p = random.getrandbits(1024) | 1
    print(f'📢 {p}')

    sharer = ShamirSecretSharing(p)

    # make x into p but with 0's in the last 1024 bits
    x = 1
    assert x % p != 0
    y = sharer.evaluate(x)
    print(f'🤝 {y}')

    solve_z3(p, x, y)

    secret = 1
    assert secret == sharer.secret

    print("Yay! You got the flag!")


def get_p(r):
    r.recvuntil('📢 '.encode())
    return int(r.recvline().decode().strip())


def get_share(r, x: int):
    r.sendlineafter('👋 '.encode(), str(x).encode())
    r.recvuntil('🤝 '.encode())
    return int(r.recvline().decode().strip())


def get_flag(r, secret: int):
    r.sendlineafter('🔑 '.encode(), str(secret).encode())


def solve():
    r = remote('chal.hkcert23.pwnable.hk', 28103)

    p = get_p(r)
    print(f'{p = }')

    x = 1
    y = get_share(r, x)
    print(f'{x = }, {y = }')

    secret = 0
    get_flag(r, secret)

    r.interactive()


if __name__ == '__main__':
    play()

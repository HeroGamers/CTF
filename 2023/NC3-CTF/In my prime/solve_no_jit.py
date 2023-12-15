from numba import njit
from typing import List, Tuple
import numpy as np


@njit
def get_primes(n: int) -> List[int]:
    # Get every prime up to n using the Sieve of Eratosthenes
    sieve = [True] * (n + 1)
    primes = []
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            sieve[p * p: n + 1: p] = [False] * ((n - p * p) // p + 1)
    return primes


@njit
def ciffer_sum(primes: List[int]) -> int:
    # Calculate the sum of the most and least significant digit of each prime
    # and sum them together
    return sum([(int(str(p)[0]) + int(str(p)[-1])) for p in primes])


@njit
def ciffer_sum2(primes: List[int]) -> int:
    # Get base 7 of each prime and sum the digits using ciffer sum, but without calling ciffer sum
    return sum(sum([int(c) for c in str(int(np.base_repr(p, 7)))]) for p in primes)


@njit
def calculation_3(primes: List[Tuple[int, int]]) -> int:
    # Multiply each prime with its nearest smaller prime (mod 31337) and sum the count of uneven numbers
    return sum([sum([1 if int(c) % 2 == 1 else 0 for c in str((p1 * p2) % 31337)]) for p1, p2 in primes])


@njit
def solve(n):
    # print(f"\n\n{n=}")
    # Du bliver givet et primtal N og skal inden for 3 sekunder
    # udføre følgende tre beregninger og svare med summen af resultaterne:
    primes = get_primes(n)
    # print(f"{primes=}")

    # Every second prime
    primes2 = primes[::-2]
    # print(f"\n{primes2=}")
    # Every third prime
    primes3 = primes[::-3]
    # print(f"{primes3=}")
    # List of tuples with every fifth prime and their nearest smallest prime
    primes5 = [(p, primes[primes.index(p) - 1]) for p in primes[::-5]]
    # print(f"{primes5=}\n")

    calc1 = ciffer_sum(primes2)
    # print(f"{calc1=}\n")
    calc2 = ciffer_sum2(primes3)
    # print(f"{calc2=}\n")
    calc3 = calculation_3(primes5)
    # print(f"{calc3=}\n")

    sol = sum((calc1, calc2, calc3))
    # print(f"{sol=}")

    return sol


def main():
    numbers = [(23, 50), (97, 178), (997, 1434), (549979, 509053)]

    for number in numbers:
        print(f"{number[0]=}")
        sol = solve(number[0])
        print(f"{sol=}")
        assert sol == number[1]


if __name__ == "__main__":
    main()

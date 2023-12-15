from numba import njit
import numpy as np
from pwn import *
import time


@njit
def get_primes(n: int) -> np.ndarray:
    # Initialize sieve array
    sieve = np.ones(n + 1, dtype=np.int32)
    sieve[0:2] = 0  # 0 and 1 are not prime

    for p in range(2, int(np.sqrt(n)) + 1):
        if sieve[p] == 1:
            sieve[p*p : n + 1 : p] = 0

    # Use np.nonzero to find prime indices
    primes = np.nonzero(sieve)[0]

    return primes


@njit
def sum_of_least_and_most_significant_digit(prime: np.int64) -> np.int64:
    # Calculate the sum of the most and least significant digit of a prime
    return np.int64(prime % 10 + prime // 10 ** (np.int64(np.log10(prime))))

@njit
def ciffer_sum(primes: np.ndarray) -> np.int64:
    # Calculate the sum of the most and least significant digit of each prime
    # and sum them together
    return np.sum(np.array([sum_of_least_and_most_significant_digit(p) for p in primes]))


@njit
def base7_conversion(number: np.int64) -> np.ndarray:
    result = [np.int64(x) for x in range(0)]
    while number > 0:
        remainder = np.int64(number % 7)
        result.insert(0, remainder)
        number //= 7
    return np.array(result, dtype=np.int64)


@njit
def ciffer_sum2(primes: np.ndarray) -> np.int64:
    # Get base 7 of each prime and sum the digits using ciffer sum, but without calling ciffer sum
    return np.sum(np.array([np.sum(base7_conversion(p)) for p in primes]))


@njit
def get_amount_of_uneven_digits(number: np.int64) -> np.int64:
    result = np.int64(0)
    while number > 0:
        remainder = np.int64(number % 10)
        if remainder % 2 == 1:
            result += 1
        number //= 10
    return result


@njit
def calculation_3(primes: np.ndarray) -> np.int64:
    # Multiply each prime with its nearest smaller prime (mod 31337) and sum the count of uneven numbers
    return np.sum(np.array([get_amount_of_uneven_digits((p1 * p2) % 31337) for p1, p2 in primes]))


@njit
def solve(n):
    # print(f"\n\n{n=}")
    # Du bliver givet et primtal N og skal inden for 3 sekunder
    # udføre følgende tre beregninger og svare med summen af resultaterne:
    # start = time.time()
    primes = get_primes(n)
    # end = time.time()
    # print("Getting primes took: " + str(end - start) + " seconds")
    # print(primes)

    # Every second prime
    # start = end
    primes2 = primes[::-2]
    # print(primes2)
    # Every third prime
    primes3 = primes[::-3]
    # print(primes3)
    # List of tuples with every fifth prime and their nearest smallest prime
    # rewrite with numpy to give an array with the primes and their nearest smaller prime
    # Extract every 5th prime in reverse order
    every_5th_prime = primes[::-5]

    # Find the indices of every 5th prime
    indices = np.arange(len(primes) - 1, -1, -5)

    # Create an array with every 5th prime and their second-smallest prime
    primes5 = np.column_stack((every_5th_prime, primes[indices - 1]))
    # primes5 = np.array([(p, primes[np.searchsorted(primes, p) - 1]) for p in primes[::5]], dtype=np.int64)
    # primes5 = [(p, primes[primes.index(p) - 1]) for p in primes[::-5]]
    # print(primes5)
    # end = time.time()
    # print("Preparing primes took: " + str(end - start) + " seconds")

    # start = end
    calc1 = ciffer_sum(primes2)
    # end = time.time()
    # print("Calculation 1 took: " + str(end - start) + " seconds")
    # print(calc1)

    # start = end
    calc2 = ciffer_sum2(primes3)
    # end = time.time()
    # print("Calculation 2 took: " + str(end - start) + " seconds")
    # print(calc2)

    # start = end
    calc3 = calculation_3(primes5)
    # end = time.time()
    # print("Calculation 3 took: " + str(end - start) + " seconds")
    # print(calc3)

    sol = np.sum(np.array([calc1, calc2, calc3]))
    # print(f"{sol=}")

    return sol

def try_solve():
    # set debug context
    context.update(arch="amd64", os="linux")
    context.log_level = "debug"

    io = remote("inmyprime.nc3", 3119)

    io.recvuntil(b"Here's the question: \n")
    n = int(io.recvline().decode().strip())
    sol = solve(n)
    io.sendline(str(sol).encode())

    io.interactive()
    # NC3{th3_numb3rs_wh4t_d0_th3y_m3an?}

def main():
    numbers = [(23, 50), (97, 178), (997, 1434), (549979, 509053)]

    for number in numbers:
        print(f"{number[0]=}")
        sol = solve(number[0])
        print(f"{sol=}")
        assert sol == number[1]

    # take timing
    print("Solving...")
    start = time.time()
    sol = solve(75241171)
    end = time.time()
    print("Done!")
    print(f"{sol=}")
    print(f"{end - start=}")

    try_solve()


if __name__ == "__main__":
    main()

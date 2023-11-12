import base64
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from pwn import xor
from sympy import Symbol, solve, Mod
from tqdm import tqdm
from z3 import *


def find_m(c1, c2, n):
    # m = Symbol('m')
    # k = Symbol('k')
    # eq1 = Mod((k * m), n) - c1
    # # eq2 = (k + m) - 2 * (k*m) - c2
    #
    # # eq2 = (k+m) % 2**1024 - (k*m) % 2**1024 - c2
    # eq2 = Mod((k+m), n) - c2
    #
    # equation = [eq1, eq2]
    # return solve(equation, [m, k])

    # Define the variable m as a symbol
    m = Symbol('m')

    # Solve the quadratic equation (m^2 - c2*m + c1) mod n = 0 for m
    solutions = solve((m ** 2 - c2 * m + c1) % n, m)

    # Iterate through the solutions to find valid m and corresponding k
    for sol in solutions:
        # Calculate k using k = (c2 - m) mod n
        k = (c2 - sol) % n

        # Check if k and m are valid by verifying equation 1
        if (k * sol) % n == c1:
            print(f"Found valid k: {k}")
            print(f"Found valid m: {sol}")
            return k, sol
            break

def solve(k, c1, c2, n):
    m = (c2 - c1) % n  # From the second equation c2 ≡ (k + m) mod n
    k_inv = inverse(k, n)  # Modular multiplicative inverse of k
    m = (m * k_inv) % n  # Solve for m using c1 ≡ k * m mod n
    return m

def find_k_and_m_3(c1, c2, n):
    k_inverse = inverse(c2 - 1, n)
    m_inverse = inverse(c1, n)
    k = (c1 * k_inverse) % n
    m = (c2 - k) % n
    return k, m

def solve_z3(c1_bytes, c2_bytes, n_prime):
    # Create a solver instance
    solver = Solver()

    # Convert the cipher bytes to long integers
    c1_long = bytes_to_long(c1_bytes)
    c2_long = bytes_to_long(c2_bytes)

    # Define BitVec variables with calculated bitwidths
    n = BitVecVal(n_prime, 1024)  # n is a prime number
    c1 = BitVecVal(c1_long, 1024)  # c1 is a long integer
    c2 = BitVecVal(c2_long, 1024)  # c2 is a long integer
    m = BitVec('m', 1024)  # m is the flag
    k = BitVec('k', 1024)  # k is the key

    # Define equations based on the provided cipher and XOR functions
    solver.add((k * m) % n == c1)  # The cipher equation
    # solver.add(k + m - 2 * (k & m) == c2)  # XOR operation equation
    solver.add(k ^ m == c2)  # XOR operation equation

    # Check if the equations are satisfiable
    if solver.check() == sat:
        # If satisfiable, get the model and extract values for m and k
        model = solver.model()
        m_value = model[m].as_long()
        k_value = model[k].as_long()

        # Print the obtained values of m and k
        print("m (flag) =", m_value)
        print("k (key) =", k_value)
    else:
        print("No solution found.")

    # solver = SolverFor("QF_BV")
    # Define BitVec variables with calculated bitwidths
    # n = BitVecVal(n_prime, 1024)  # n is a prime number
    # c1 = BitVecVal(c1_long, 1024)  # c1 is a long integer
    # c2 = BitVecVal(c2_long, 1024)  # c2 is a long integer
    # m = BitVec('m', 1024)  # m is the flag
    # k = BitVec('k', 1024)  # k is the key

def solve_z3_2(c1_bytes, c2_bytes, n_prime):
    # Create a solver instance
    solver = Solver()

    # Convert the cipher bytes to long integers
    c1_long = bytes_to_long(c1_bytes)
    c2_long = bytes_to_long(c2_bytes)

    n = n_prime
    c1 = c1_long
    c2 = c2_long

    m = Int('m')  # m is the flag
    k = Int('k')  # k is the key

    # Solve the modular multiplication equation
    solver.add((k * m) % n == c1)
    # Solve the XOR equation
    solver.add(k + m == c2)

    # Check if the equations are satisfiable
    if solver.check() == sat:
        # Get the model and extract the values for m and k
        model = solver.model()
        m_value = model[m].as_long()
        k_value = model[k].as_long()

        # Print the obtained values of m and k
        print("m (flag) =", m_value)
        print("k (key) =", k_value)
    else:
        print("No solution found for the given equations.")


# from_range = 351557825396366065905977571421142037038514170164853294186450534129269956270574273168644083034382965609605364508135091656758615092639235325864988731544562196349
#     for m in tqdm(range(from_range, n), total=n, initial=from_range):

def manual_solve(c1, c2, n):
    for m in range(n):
        k = (c2 - m) % n
        if (k * m) % n == c1:
            print(f"Found valid k: {k}")
            print(f"Found valid m: {m}")
            break


def solve_equation(c1, c2, n):
    discriminant = c2 ** 2 - 4 * (c1 - n)

    if discriminant < 0:
        return None, None  # No real solutions

    sqrt_discriminant = math.isqrt(discriminant)
    x1 = (c2 + sqrt_discriminant) // 2
    x2 = (c2 - sqrt_discriminant) // 2

    print(x1)
    print(x2)

    return x1, x2


def main():
    # Provided values
    with open("output.txt", "r") as output:
        c1 = base64.b64decode(output.readline().split(" = ")[1].strip())
        c2 = base64.b64decode(output.readline().split(" = ")[1].strip())
        n = int(output.readline().split(" = ")[1].strip())

        print(f"c1: {c1}")
        print(f"c2: {c2}")
        print(f"n: {n}")

    # solve_z3_2(c1, c2, n)
    # manual_solve(bytes_to_long(c1), bytes_to_long(c2), n)

    solve_equation(bytes_to_long(c1), bytes_to_long(c2), n)

    # c1 = bytes_to_long(c1)
    # c2 = bytes_to_long(c2)
    # print(c1)
    # print(c2)
    #
    # # sol = find_m(c1, c2, n)
    # sol = find_k_and_m_3(c1, c2, n)
    #
    # print(sol)
    #
    # flag = long_to_bytes(sol[1])
    # key = long_to_bytes(sol[0])
    #
    # print(f"flag: {flag}")
    # print(f"key: {key}")


if __name__ == '__main__':
    main()

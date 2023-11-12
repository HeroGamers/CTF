N = 102
MOD = 1000000007

def solve(m: int, n: int, a: list):
    dp = [[0] * n for _ in range(m)]

    non_zero_count = 0

    dp[0][0] = 1 if a[0][0] != 'x' else 0
    for i in range(m):
        for j in range(n):
            if a[i][j] == 'x':
                continue
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
            if dp[i][j]:
                non_zero_count += 1

    print(non_zero_count)
    for i in range(m):
        for j in range(n):
            if dp[i][j] > 0:
                print(f"{i} {j} {dp[i][j]}")

def generate_input_file(m, n, a, save=True):
    output = f"{m} {n}\n"
    for i in range(len(a)):
        output += ''.join(a[i]) + '\n'
    if save:
        with open("input.txt", "w") as f:
            f.write(output)
    print(output)

def read_input_file():
    with open("input.txt", "r") as f:
        m, n = map(int, f.readline().split())
        a = [list(f.readline().strip()) for _ in range(m)]
    return m, n, a

def generate_input(m, n):
    a = [['.'] * n for _ in range(m)]
    a[1][0] = 'x'
    return a

def main():
    # m = 100
    # n = 3
    #
    # a = generate_input(m, n)
    #
    # generate_input_file(m, n, a)
    m, n, a = read_input_file()

    generate_input_file(m, n, a, save=False)

    solve(m, n, a)

if __name__ == "__main__":
    main()
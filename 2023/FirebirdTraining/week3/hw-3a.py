# Reversed through Ghidra
data = b'\x55\x38\x5b\x31\xb1\x8e\xb3\xed\x8b\x1d\xaf\x50\x6e\xb6\x25\x6a\xf6\x79\xec\x4e\x6f\x1b\x2a\x6e\xe4\x74\x08\xbf\x8d'

print(f"Data: \t\t\t\t{[data[i] for i in range(29)]}")

# Initialize the Fibonacci sequence
# Create an array to store the Fibonacci numbers
# f = b'\x01\x01\x02\x03\x05\x08\x0d\x15\x22\x37\x59\x90\xe9\x79\x62\xdb\x3d\x18\x55\x6d\xc2\x2f\xf1\x20\x11\x31\x42\x73\xb5\x00\x00\x00'

# print(f"Fibonacci: \t\t\t{[f[i] for i in range(29)]}")

fibonacci = [0] * 32
fibonacci[0] = 1
fibonacci[1] = 1

# Calculate the Fibonacci sequence with overflow
for i in range(2, 32):
    fibonacci[i] = (fibonacci[i - 1] + fibonacci[i - 2]) % 256

charset = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}+/'

print(f"Fibonacci: \t\t\t{[fibonacci[i] for i in range(29)]}")

# Initialize the input string
input = [48] * 29
input[0] = ord('f')
input[1] = ord('l')
input[2] = ord('a')
input[3] = ord('g')
input[4] = ord('{')
input[-1] = ord('}')

print(f"Input: \t\t\t\t{input}")

# Calculate the input string
for i in range(29):
    input[i] = (input[i] + fibonacci[i]) % 256

print(f"Modified input: \t{input}")

input_raw = input.copy()

# Decrypt the input string
for i in range(29):
    # possible_chars = []
    # for char_1 in charset:
    #     for char_2 in charset:
    #         if char_1 ^ char_2 == data[i]:
    #             possible_chars.append((char_1, char_2))
    # print(f"{i}: {possible_chars}")

    if input[i] ^ input[(i + 28) % 29] == data[i]:
        input[i] = input[i] ^ input[(i + 28) % 29]
        print("YAY")
    else:
        for j in range(256):
            if j ^ input[(i + 28) % 29] == data[i]:
                input[i] = j
                input_raw[i] = j
                input[i] = input[i] ^ input[(i + 28) % 29]
                break

print(f"Final input: \t\t{input}")
print(f"Final input: \t\t{''.join([chr((input_raw[i]-fibonacci[i]) % 256) for i in range(29)])}")

# Check if the input matches the data
if all(input[i] == data[i] for i in range(29)):
    print(":D")
else:
    print(":(")

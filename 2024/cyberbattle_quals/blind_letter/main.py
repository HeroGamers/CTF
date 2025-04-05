INPUT = "⠼⠊⠼⠑⠼⠃⠼⠑⠼⠓⠼⠋⠼⠋⠼⠋⠼⠙⠼⠊⠼⠙⠼⠚⠼⠚⠼⠓⠼⠉⠼⠛⠼⠊⠼⠚⠼⠋⠼⠉⠼⠛⠼⠊⠼⠃⠼⠃⠼⠁⠼⠉⠼⠙⠼⠊⠼⠚⠼⠃⠼⠙⠼⠚⠼⠙⠼⠊⠼⠚⠼⠃⠼⠑⠼⠚⠼⠋⠼⠉⠼⠊⠼⠛⠼⠃⠼⠉⠼⠃⠼⠑⠼⠃⠼⠊⠼⠛⠼⠑⠼⠁⠼⠛⠼⠋⠼⠊⠼⠉"

braile_dict = {
    "⠁": "a",
    "⠃": "b",
    "⠉": "c",
    "⠙": "d",
    "⠑": "e",
    "⠋": "f",
    "⠛": "g",
    "⠓": "h",
    "⠊": "i",
    "⠚": "j",
    "⠅": "k",
    "⠇": "l",
    "⠍": "m",
    "⠝": "n",
    "⠕": "o",
    "⠏": "p",
    "⠟": "q",
    "⠗": "r",
    "⠎": "s",
    "⠞": "t",
    "⠥": "u",
    "⠧": "v",
    "⠺": "w",
    "⠭": "x",
    "⠽": "y",
    "⠵": "z",
    "⠼": " ",
}

char_to_decimal = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    " ": 11,
}

decimal_to_binary = {
    0: "0000",
    1: "0001",
    2: "0010",
    3: "0011",
    4: "0100",
    5: "0101",
    6: "0110",
    7: "0111",
    8: "1000",
    9: "1001",
    10: "1010",
    11: "1011",
}

def decode_braile(input: str) -> str:
    return "".join([braile_dict[char] for char in input])

if __name__ == "__main__":
    output = decode_braile(INPUT)
    print(output)
    print(output.replace(' ', ''))
    # count unique characters
    print(len(set(output)))
    # sort characters
    print(sorted(set(output)))

    # convert to decimal
    decimals = [char_to_decimal[char] for char in output]
    print(decimals)
    print(' '.join([str(decimal) for decimal in decimals]))

    # convert to binary
    binary = [bin(decimal)[2:] for decimal in decimals]
    print(binary)

    # as single string
    binary_str = "".join(binary)
    # make a space every 8 characters
    binary_str = " ".join([binary_str[i:i+8] for i in range(0, len(binary_str), 8)])
    print(binary_str)

    # use the other dictionary to convert to binary
    binary_str = "".join([decimal_to_binary[decimal] for decimal in decimals])
    print(binary_str)
    # make a space every 8 characters
    binary_str = " ".join([binary_str[i:i+8] for i in range(0, len(binary_str), 8)])
    print(binary_str)
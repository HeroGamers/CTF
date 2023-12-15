# Import color so we can print in color
from colorama import Fore, Style

substitution = {
    "C": "N",
    "}": "C",
    "n": "3",
    "6": "{",
    "h": "}",
    "g": "c",
    "e": "h",
    "J": "r",
    "m": "i",
    "X": "s",
    "7": "t",
    "I": "m",
    "5": "a",
    "b": "e",
    "B": "y",
    "2": "o",
    "G": "f",
    "j": "b",
    "(": "w",
    "r": "v",
    "u": "u",
    ")": "M",
    "1": "n",
    "y": "z",
    "W": "l",
    "O": "W",
    "l": "k",
    "a": "g",
    "8": "d",
    "4": "p",
    "f": "j",
    "U": "T",
    "T": "I",
    "k": "a",
    "M": "J",
    "K": "B",
    "H": "V",
    "Q": "1",
    "V": "2",
    "q": "(",
    "R": ")",
    "t": "O",
    "0": "x",
    "F": "F",
    "A": "T",
    "N": "N"
}

def main():
    with open("besked.txt") as file:
        encoded = file.read().strip()

    # Substitution, but we need to do it all in one go so we don't mess up the
    # substitutions
    decoded = "".join((Fore.RED + substitution.get(c, Style.RESET_ALL + c)) for c in encoded)
    # let's rewrite it to color the substitutions


    print(decoded)


if __name__ == '__main__':
    main()

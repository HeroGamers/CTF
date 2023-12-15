import base64

from colorama import Fore, Style

secret_message = """
55 62 69 20 75 62 69 21 20 53 62 65 66 62 72 74 72 65 20 71 68 20 6e 67 20 66 61 6c 71 72 3f 20 46 78 6e 7a
20 71 76 74 2e 20 5a e5 66 78 72 20 72 65 20 71 68 20 66 79 72 67 20 76 78 78 72 20 66 e5 20 71 6c 74 67 76
74 20 66 62 7a 20 71 68 20 63 e5 66 67 e5 65 21 20 42 75 20 6a 72 79 79 2c 20 7a 72 61 20 71 68 20 73 62 65
67 77 72 61 72 65 20 69 72 79 20 72 67 20 75 76 61 67 3a 20 49 78 35 4f 47 76 4f 63 70 61 53 35 71 61 45 6c
71 4a 57 35 70 4b 57 79 56 55 57 75 56 55 79 32 4d 7a 71 6c 56 54 35 6d 56 54 35 35 72 4b 56 74 4c 61 41 6d
71 61 4f 32 70 61 79 61 56 54 49 6c 71 55 4d 7a 4d 33 57 79 70 7a 70 74 4c 32 57 79 4d 33 56 66 56 54 41 79
4c 7a 71 76 72 54 57 35 72 4b 57 79 56 54 57 30 56 54 4d 6c 4d 4a 79 32 70 55 57 7a 59 76 4f 6e 35 4a 4d 34
70 76 4f 6b 70 7a 52 74 72 4b 4d 7a 4d 33 56 74 72 54 35 75 56 55 49 33 35 61 79 77 70 76 4f 6b 71 61 44 68
"""

substitution = {
    "u": "h",
    "b": "o",
    "i": "v",
    "z": "m",
    "å": "å",
    "f": "s",
    "x": "k",
    "r": "e",
    "v": "i",
    "e": "r",
    "q": "d",
    "h": "u",
    "l": "y",
    "t": "g",
    "g": "t",
    "c": "p",
    "y": "l",
    "n": "a",
    "s": "f",
    "a": "n",
    "w": "j",
    "j": "w",
    "m": "z",
    "p": "c",
    "k": "x",
    "d": "q",
    "o": "b",
    "æ": "æ"
}

# Decrypt the secret message
message = bytes.fromhex(secret_message.replace("\n", "").replace(" ", "")).replace(b"\xe5", b"_").decode().replace("_",
                                                                                                                   "å")
print(message)


def subs(c):
    return (Fore.RED + (substitution.get(c.lower()).upper() if c.isupper() else substitution.get(c.lower()))) if substitution.get(c.lower(), None) else (Style.RESET_ALL + c)


decoded = "".join(subs(c) for c in message) + Style.RESET_ALL
print(decoded)
# Hov hov! Forsoeger du at snyde? Skam dig. Måske er du slet ikke så dygtig som du påstår! Oh well, men du fortjener vel et hint:
# Vk5BTiBpcnF5dnRydWJ5cXJlIHJhIHl2ZmdyIG5zIG55eXIgYnNzdnB2cnlnIGVydHZmZ3JlcmcgY2JlZ3IsIGNlYmdieGJ5eXJlIGJ0IGZyZWl2cHJmLiBa5WZ4ciBxcmEgeXZmZ3IgeG5hIHV35nljciBxdnQu

new_message = "Vk5BTiBpcnF5dnRydWJ5cXJlIHJhIHl2ZmdyIG5zIG55eXIgYnNzdnB2cnlnIGVydHZmZ3JlcmcgY2JlZ3IsIGNlYmdieGJ5eXJlIGJ0IGZyZWl2cHJmLiBa5WZ4ciBxcmEgeXZmZ3IgeG5hIHV35nljciBxdnQu"
print(new_message)

# Base64 decode
base64_decoded = base64.b64decode(new_message).replace(b"\xe5", b"_").replace(b"\xe6", b"-").decode().replace("_", "å").replace("-", "æ")
print(base64_decoded)

decoded = "".join(subs(c) for c in base64_decoded) + Style.RESET_ALL
print(decoded)
# IANA vedligeholder en liste af alle officielt registeret porte, protokoller og services. Måske den liste kan hjælpe dig.
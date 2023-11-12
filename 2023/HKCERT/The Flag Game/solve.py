# We need functions for sha224 and sha256
from Crypto.Hash import SHA224, SHA256

HASH_CHECKS = [
    {
        "length": 8,
        "hash": SHA224,
        "starts_with": "b08c89",
    },
    {
        "length": 10,
        "hash": SHA224,
        "starts_with": "ce45fd",
    },
    {
        "length": 12,
        "hash": SHA256,
        "starts_with": "87b3c7",
    },
    {
        "length": 14,
        "hash": SHA256,
        "starts_with": "d0687a",
    },
    {
        "length": 16,
        "hash": SHA256,
        "starts_with": "cbe2c9",
    },
    {
        "length": 18,
        "hash": SHA256,
        "starts_with": "c25dd2",
    },
    {
        "length": 20,
        "hash": SHA256,
        "starts_with": "b72709",
    },
    {
        "length": 22,
        "hash": SHA224,
        "starts_with": "8b035b",
    },
    {
        "length": 24,
        "hash": SHA256,
        "starts_with": "40f34c",
    },
    {
        "length": 26,
        "hash": SHA256,
        "starts_with": "7be965",
    },
    {
        "length": 28,
        "hash": SHA224,
        "starts_with": "0b67cb",
    },
    {
        "length": 30,
        "hash": SHA224,
        "starts_with": "bf7eeb",
    },
    {
        "length": 32,
        "hash": SHA256,
        "starts_with": "f9f48b",
    },
    {
        "length": 34,
        "hash": SHA224,
        "starts_with": "69260f",
    },
    {
        "length": 36,
        "hash": SHA256,
        "starts_with": "7ef31a",
    },
    {
        "length": 38,
        "hash": SHA256,
        "starts_with": "e3c817",
    },
    {
        "length": 40,
        "hash": SHA224,
        "starts_with": "8a9de8",
    },
    {
        "length": 42,
        "hash": SHA256,
        "starts_with": "e3c817",
    },
]

FLAG_START = "hkcert23{"
# sorted by usage in English alphabet and removed those which rules say are not to be used (upper-case) and "fail"
CHARSET = "3e7t40o1n5srhdcump_gwybvkxjqz2689}"

def check_hash(hash_check, flag):
    hash_func = hash_check["hash"]
    starts_with = hash_check["starts_with"]
    length = hash_check["length"]
    string_subset = flag[:length]
    hash_obj = hash_func.new(string_subset.encode())
    return hash_obj.hexdigest().startswith(starts_with)


def main():
    flag = FLAG_START
    for hash_check in HASH_CHECKS:
        chars_to_guess = hash_check["length"] - len(flag)
        print(f"Trying to find {chars_to_guess} chars for {hash_check['length']}")
        if chars_to_guess <= 0:
            if not check_hash(hash_check, flag):
                print(f"Failed at {hash_check['length']} for flag {flag}")
                return
        else:
            # loop through charset and try each char for amount of chars_to_guess
            if chars_to_guess == 1:
                for char in CHARSET:
                    flag_to_check = flag + char
                    if check_hash(hash_check, flag_to_check):
                        flag = flag_to_check
                        print(f"Found char {char} for {hash_check['length']}!")
                        print(f"Flag is now {flag}")
                        break
                else:
                    print(f"Could not find a valid char for {hash_check['length']}!")
            elif chars_to_guess == 2:
                found = False
                for char1 in CHARSET:
                    for char2 in CHARSET:
                        flag_to_check = flag + char1 + char2
                        if check_hash(hash_check, flag_to_check):
                            flag = flag_to_check
                            print(f"Found chars {char1}{char2} for {hash_check['length']}!")
                            print(f"Flag is now {flag}")
                            found = True
                            break
                    if found:
                        break
                else:
                    print(f"Could not find valid chars for {hash_check['length']}!")
            elif chars_to_guess == 3:
                found = False
                for char1 in CHARSET:
                    for char2 in CHARSET:
                        for char3 in CHARSET:
                            flag_to_check = flag + char1 + char2 + char3
                            if check_hash(hash_check, flag_to_check):
                                flag = flag_to_check
                                print(f"Found chars {char1}{char2}{char3} for {hash_check['length']}!")
                                print(f"Flag is now {flag}")
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                else:
                    print(f"Could not find valid chars for {hash_check['length']}!")
            else:
                print("bruh?")
                return
    print(f"Final flag is: {flag}")


if __name__ == '__main__':
    main()

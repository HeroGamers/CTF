map = {
    'g': 'f',
    'z': 'l',
    'f': 'a',
    'm': 'g',
    "b": "w",
    "c": "k",
    "d": "h",
    "w": "p",
    "e": "u",
    "s": "y",
    "l": "r",
    "x": "s",
    "o": "s",
    "i": "i",
    "j": "b",
    "v": "n"

# flag{w33k_4_h0p3_u_guy5_r_sti11_br3ath1ng}
# gzfm{b33c_4_d0w3_e_mes5_l_xoi11_jl3fod1vm}
}




if __name__ == "__main__":
    with open("attendence-4-trackb.txt", "r") as attendance_trackb:
        # read in
        lines = attendance_trackb.read()
    # Switch letters around until it makes sense
    # based on frequence of letters in the English alphabet
    # https://en.wikipedia.org/wiki/Letter_frequency

    print(lines)

    letter_count = {}
    # 1. Count the frequency of each letter
    for letter in lines:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1

    # 2. Sort the letters by frequency
    sorted_letter_count = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
    print(sorted_letter_count)

    # 4. Decrypt the message
    decrypted_message = ""
    for letter in lines:
        decrypted_message += map[letter] if letter in map else letter
    print(decrypted_message)

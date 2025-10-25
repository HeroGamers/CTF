from pwn import remote
from extendedrandcrack import ExtendedRandCrack

HOST = 'localhost'
PORT = 777

def extract_number(line):
    import re
    m = re.search(r'Number was (\d+)', line)
    return int(m.group(1)) if m else None

def main():
    r = remote(HOST, PORT)
    rc = ExtendedRandCrack()

    # Wait until menu
    while True:
        line = r.recvline(timeout=3).decode()
        print(line.strip())
        if 'Menu' in line:
            break

    hl_plays_left = 1000
    outputs = 0
    predicted = False

    while hl_plays_left > 0:
        print(f"Plays left: {hl_plays_left}, Outputs collected: {outputs}")
        r.sendline(b'1')  # Choose High-Low

        r.recvuntil(b'bet (1-10):')
        r.sendline(b'10')

        r.recvuntil(b'> ')

        if predicted:
            predicted_num = rc.predict_getrandbits(32)
            guess = 'L' if predicted_num < 2147483647 else 'H'
            print(f"Predicted number {predicted_num}, guessing {guess}")
            r.sendline(guess.encode())
        else:
            r.sendline(b'L')  # seed with arbitrary guess

        # Wait for result line containing number
        while True:
            result_line = r.recvline(timeout=3).decode().strip()
            print(result_line)
            if "Number was" in result_line:
                break

        num = extract_number(result_line)
        if num is None:
            print("Failed to extract number. Exiting.")
            break

        if outputs < 624:
            rc.submit(num)
            outputs += 1

        rem_line = r.recvline().decode()
        print(rem_line.strip())
        hl_plays_left -= 1

        if outputs >= 624:
            predicted = True

        # Clear any extra lines before menu prompt
        while True:
            line = r.recvline(timeout=1)
            if not line or b"Menu" in line:
                break
            print(line.decode(errors='ignore').strip())

    # Read flag if any
    try:
        while True:
            line = r.recvline(timeout=3).decode()
            print(line.strip())
            if "DREAM{" in line:
                print("FLAG:", line.strip())
                break
    except:
        pass

    r.close()

if __name__ == "__main__":
    main()

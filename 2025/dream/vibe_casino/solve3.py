from pwn import remote, context
from extendedrandcrack import ExtendedRandCrack
import re

HOST = 'vibecasino.meowmeow.mvm.lol'
PORT = 31337


context.log_level = 'debug'

def get_coins(r):
    r.sendline(b'3')
    line = r.recvline(timeout=2).decode().strip()
    print(f"[get_coins] line: {line}")
    m = re.search(r'You have (\d+) coins\.', line)
    if m:
        coins = int(m.group(1))
        print(f"[+] Synced coins: {coins}")
        return coins
    else:
        print("[!] Failed to parse coins from balance command output")
        return None

def extract_number(line):
    m = re.search(r'Number was (\d+)', line)
    return int(m.group(1)) if m else None

# CPython's Random.random() uses two 32-bit MT outputs:
# a = getrandbits(32) >> 5  # 27 bits
# b = getrandbits(32) >> 6  # 26 bits
# return ((a << 26) | b) / 2**53
# Implement this to stay perfectly in sync with random.choices

def predict_random_cpython(rc: ExtendedRandCrack) -> float:
    a = rc.predict_getrandbits(32) >> 5  # 27 bits
    b = rc.predict_getrandbits(32) >> 6  # 26 bits
    return ((a << 26) | b) / (1 << 53)

def weighted_choice(weights, rc):
    total = sum(weights)
    r = predict_random_cpython(rc) * total
    upto = 0
    for i, w in enumerate(weights):
        if upto + w > r:
            return i
        upto += w
    return len(weights) - 1

def predict_slots(rc):
    weights = [464, 200, 180, 156]
    symbols = ["7", "A", "B", "C"]
    result = []
    for _ in range(3):
        idx = weighted_choice(weights, rc)
        result.append(symbols[idx])
    return result

def main():
    r = remote(HOST, PORT, ssl=True)
    rc = ExtendedRandCrack()

    # Wait until menu
    while True:
        line = r.recvline(timeout=5).decode()
        print(line.strip())
        if 'Menu' in line:
            break

    hl_plays_left = 1000
    outputs = 0
    predicted = False

    while True:
        print(f"Plays left: {hl_plays_left}, Outputs collected: {outputs}")
        if hl_plays_left > 0:
            # Play High-Low (always bet 1 to avoid insufficient funds issues)
            r.sendline(b'1')
            r.recvuntil(b'bet (1-10):')
            bet = 1
            r.sendline(b'1')

            r.recvuntil(b'> ')

            if predicted:
                # Use the next random number directly - randint(0, 4294967294) 
                # should consume exactly one 32-bit output
                predicted_num = rc.predict_getrandbits(32)
                # The range is [0, 4294967294] which is [0, 2^32-2]
                # Python's randint should map this directly
                if predicted_num > 4294967294:
                    predicted_num = predicted_num % 4294967295

                guess = 'L' if predicted_num < 2147483647 else 'H'
                print(f"Predicting High-Low number {predicted_num}, guessing {guess}")
                r.sendline(guess.encode())
            else:
                r.sendline(b'L')

            # Receive result with number
            while True:
                res_line = r.recvline(timeout=5).decode().strip()
                print(res_line)
                if "Number was" in res_line:
                    break

            num = extract_number(res_line)
            if num is None:
                print("Failed to extract number, exiting.")
                break

            # Assert prediction matches actual if we're in prediction mode
            if predicted:
                actual_num = num
                expected_num = predicted_num
                print(f"Prediction check: expected {expected_num}, actual {actual_num}")
                assert expected_num == actual_num, f"High-Low prediction mismatch! Expected {expected_num}, got {actual_num}"

            if outputs < 624:
                rc.submit(num)
                outputs += 1
                if outputs == 624:
                    print("[*] Recovered RNG state! Starting prediction mode.")
                    predicted = True
            elif not predicted:
                print("[*] This should not happen - we should have 624 outputs by now")
                predicted = True

            # Skip any extra lines until menu
            while True:
                line = r.recvline(timeout=1)
                if not line or b"Menu" in line:
                    break

            hl_plays_left -= 1

        else:
            # Predict slots BEFORE starting the slot game
            predicted_result = predict_slots(rc)
            print(f"Predicting slots: {' '.join(predicted_result)}")
            
            # Play Slots predictively
            r.sendline(b'2')
            # Read the bet prompt - might contain multiple lines
            prompt_data = r.recvuntil(b': ', timeout=5).decode().strip()
            print(prompt_data)
            
            m = re.search(r'Enter your bet \(1-(\d+)\)', prompt_data)
            bet_max = int(m.group(1)) if m else 1

            bet = bet_max if predicted_result == ["7", "7", "7"] else 1
            print(f"Betting {bet} coins (max available: {bet_max}) - Predicted: {' '.join(predicted_result)}")
            r.sendline(str(bet).encode())

            slot_line = r.recvline(timeout=5).decode().strip()
            print(slot_line)

            # Extract actual slot result and compare with prediction
            slot_match = re.search(r'Slot: (\w) (\w) (\w)', slot_line)
            if slot_match:
                actual_result = [slot_match.group(1), slot_match.group(2), slot_match.group(3)]
                print(f"Prediction check: expected {predicted_result}, actual {actual_result}")
                assert predicted_result == actual_result, f"Slot prediction mismatch! Expected {predicted_result}, got {actual_result}"
            else:
                print("Failed to parse slot result!")
                print(f"Slot line was: '{slot_line}'")

            jackpot_line = r.recvline(timeout=5).decode().strip()
            print(jackpot_line)

            payout_line = r.recvline(timeout=5).decode().strip()
            print(payout_line)

            # Flush until menu
            while True:
                line = r.recvline(timeout=1)
                if not line or b"Menu" in line:
                    break
                print(line.decode(errors='ignore').strip())

    # Read flag message
    try:
        while True:
            line = r.recvline(timeout=5).decode().strip()
            print(line)
            if "DREAM{" in line:
                print("FLAG:", line)
                break
    except:
        pass

    r.close()

if __name__ == "__main__":
    main()
    # DREAM{you_broke_the_house}

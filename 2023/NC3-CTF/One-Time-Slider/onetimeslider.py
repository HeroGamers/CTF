import secrets
from typing import Optional
import json
import z3


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def encrypt(flag: list[int], otp: Optional[bytes] = None) -> str:
    n = len(flag)
    if otp is None:
        otp = secrets.token_bytes(n)

    print(f"{flag=}")
    print(f"{otp.hex()=}")
    # Slide OTP henover plaintext og XOR krypter alt, der er indenfor den
    for i in range(2 * n + 1):
        from_index = max(0, i - n)
        print(f"[{i}] flag[{from_index}:{i}]={flag[from_index:i]}")
        print(f"[{i}] otp[-{i}:]={list(otp[-i:])}")
        xor_res = xor(flag[from_index:i], otp[-i:])
        print(f"[{i}] Replacing flag[{from_index}:{i}] with flag[{from_index}:{i}] ^ otp[-{i}:] = {xor_res}\n")
        flag[from_index:i] = xor_res

    return bytes(flag).hex()


def calculate_depends_on(encrypted: str, otp: bytes) -> None:
    flag = list(bytes.fromhex(encrypted))
    n = len(flag)
    print(f"{flag=}")
    print(f"{list(otp)=}")

    depends_on = {}
    for i in range(n):
        depends_on[i] = []
    for i in range(2 * n + 1):
        from_index = max(0, i - n)
        flag_slice = flag[from_index:i]
        otp_slice = otp[-i:]
        print(f"{list(otp_slice)=}")
        xor_zip = list(zip(flag_slice, otp_slice))
        print(f"[{i}] {xor_zip=}")
        for j, (x, y) in enumerate(xor_zip):
            print(from_index + j, (-i) + j, j, -(i % n) + j)
            print((-i) + j >= -n)
            index_choice = ((-i) + j if ((-i) + j) == (-(i % n) + j) else j) % n
            calc_y = otp[index_choice]
            calc_x = flag[from_index + j]
            print(f"[{i}] flag[{from_index + j}]=({x} vs. {calc_x}) ^ otp[{(-i) + j}]=({y} vs. {calc_y})")
            assert y == calc_y
            assert x == calc_x
            depends_on[from_index + j].append(index_choice)
    print(depends_on)


def crack_otp(encrypted: str) -> bytes:
    # Crack the OTP using Z3
    encrypted_flag = list(bytes.fromhex(encrypted))
    n = len(encrypted_flag)

    # From looking at how the OTP is used, we know that to get the flag,
    # we XOR the bytes in the flag with the bytes in the OTP, starting from the end of the OTP.
    # We also know that the OTP is the same length as the flag.
    # We can use this to create a Z3 solver that will find the OTP.

    # Create a Z3 solver
    solver = z3.Solver()

    # Create a list of Z3 bit vectors, one for each byte in the flag
    flag = [z3.BitVec(f'flag_{i}', 8) for i in range(n)]
    # Create a list of Z3 bit vectors, one for each byte in the OTP
    otp = [z3.BitVec(f'otp_{i}', 8) for i in range(n)]

    # Create a list of Z3 bit vectors, one for each byte in the encrypted flag
    encrypted_flag = [z3.BitVecVal(c, 8) for c in encrypted_flag]

    # Set up the solver to find a solution to the following equation:
    for i in range(n):
        for j in range(n - 1, -1, -1):
            # flag[i] ^ otp[j] == encrypted_flag[i]
            solver.add(flag[i] ^ otp[j] == encrypted_flag[i])

    # Add a constraint that all bytes in the flag must be printable ASCII characters
    for i in range(n):
        solver.add(z3.And(flag[i] >= 32, flag[i] <= 126))

    # Add constraint that flag starts with "NC3{"
    solver.add(flag[0] == ord('N'))
    solver.add(flag[1] == ord('C'))
    solver.add(flag[2] == ord('3'))
    solver.add(flag[3] == ord('{'))
    solver.add(flag[n-1] == ord('}'))

    # Check if the solver can find a solution
    if solver.check() == z3.sat:
        # Get the solution
        model = solver.model()

        # Convert the solution to a Python list of bytes
        otp = [model.eval(otp[i]).as_long() for i in range(n)]
        print(f"Cracked OTP: {bytes(otp).hex()}")
        return bytes(otp)
    else:
        raise Exception("Failed to crack OTP")


def decrypt(encrypted: str, otp: Optional[bytes] = None) -> None:
    flag = list(bytes.fromhex(encrypted))
    n = len(flag)
    if otp is None:
        otp = crack_otp(encrypted)

    # otp = list(otp[:n//2])
    # otp += [0 for _ in range(n-len(otp))]
    # otp = bytes(otp)

    # for i in range(2 * n + 1):
    #     from_index = max(0, i - n)
    #     xor_res = xor(flag[from_index:i], otp[-i:])
    #     flag[from_index:i] = xor_res

    for i in range(n):
        for j in range(n-1, -1, -1):
            flag[i] ^= otp[j]

    print(f"Decrypted flag: {bytes(flag)}")


def main():
    encrypted = ""
    otp = None
    encrypted = "e9e494dcd1c2c9d3f8d1c6d5f8c3c2d3f8c3d2cad3f8c6d3f8ffe8f5f8c6cbcbc2f8c5ded3c2d4f8cac2c3f8cfd1c2d5f8ccc2def8c5ded3c2989898da"

    if not encrypted:
        with open("flag.txt", "rb") as f:
            flag = list(f.read().strip())
        print(f"{flag=}")
        otp = secrets.token_bytes(len(flag))
        encrypted = encrypt(flag, otp)

    print(f"{encrypted=}")
    if otp:
        print(f"{otp.hex()=}")

    # calculate_depends_on(encrypted, otp)
    decrypt(encrypted, otp=otp)

    # NC3{vent_var_det_dumt_at_XOR_alle_bytes_med_hver_key_byte???}


if __name__ == "__main__":
    main()

def decode_input(encoded_input: bytes):
    def decode_base64(encode_64_input: bytes):
        try:
            block_padded64 = encode_64_input + b'=' * ((4 - len(encode_64_input) % 4) % 4)
            # print(f"[DEBUG] Trying to decode to base64: {block_padded64}")
            try_decoded = base64.b64decode(block_padded64)
            # Check for valid UTF-8 characters
            char_check = try_decoded.decode("utf-8")
            for char in char_check:
                if not (ord('0') <= ord(char) <= ord('9')) and not (ord('a') <= ord(char) <= ord('z')) and not (
                        ord('A') <= ord(char) <= ord('Z')) and not char == '=':
                    raise Exception(f"Invalid character: {char} in {char_check}")
            # print(f"[DEBUG] Successfully decoded to base64: {try_decoded}")
            return try_decoded
        except Exception as e:
            # print(f"[DEBUG] Failed to decode to base64: {e}")
            return b''

    def decode_base32(encode_32_input: bytes):
        try:
            block_uppercase = encode_32_input.upper()
            block_padded = block_uppercase + b'=' * ((8 - len(block_uppercase) % 8) % 8)
            # print(f"[DEBUG] Trying to decode to base32: {block_padded}")
            try_decoded = base64.b32decode(block_padded)
            char_check = try_decoded.decode("utf-8")
            for char in char_check:
                if not (ord('0') <= ord(char) <= ord('9')) and not (ord('a') <= ord(char) <= ord('z')) and not (
                        ord('A') <= ord(char) <= ord('Z')) and not char == '=':
                    raise Exception(f"Invalid character: {char} in {char_check}")
            # print(f"[DEBUG] Successfully decoded to base32: {try_decoded}")
            return try_decoded
        except Exception as e:
            # print(f"[DEBUG] Failed to decode to base32: {e}")
            return b''

    # For reverting
    last_decoded = []
    last_i = []

    i = 0
    current_encoded_input = encoded_input
    while True:
        if not current_encoded_input:
            break
        if current_encoded_input.isdigit():
            break

        # If there is already padding, we strip it as we calculate padding ourselves.
        if b'=' in current_encoded_input:
            current_encoded_input = current_encoded_input[:current_encoded_input.index(b'=')]

        decoded = b""
        current_try_decode = b""

        # print(f"[INFO] NEW LOOP WITH: {current_encoded_input[:100]}")

        while current_encoded_input:
            try_decoded = decode_base64(current_encoded_input[i:i+4+1])
            if try_decoded:
                # Save last state if we need to revert
                last_i.append(i)
                last_decoded.append(len(decoded))

                # Update state
                decoded += try_decoded
                i += 4
            else:
                # Add 4 characters to the current try decode and try again with base32
                try_decoded = decode_base32(current_encoded_input[i:i+8+1])
                if try_decoded:
                    decoded += try_decoded
                else:
                    # Go back to last state and try again with base32
                    success = False
                    while len(last_i) > 0 and not success:
                        # Try to revert and try with base32
                        i = last_i.pop() if last_i else 0
                        decoded = decoded[:(last_decoded.pop() if last_decoded else 0)]

                        # Add 4 characters

                        # Try to decode
                        try_decoded = decode_base32(current_encoded_input[i:i+8+1])
                        if try_decoded:
                            decoded += try_decoded
                            success = True
                    if success:
                        continue
                    print("NO PROGRESS, STOPPING!")
                    exit()
                i += 8

        current_encoded_input = decoded
        i = 0
    return current_encoded_input
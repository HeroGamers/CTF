def extract_and_decode_flaggy(data):
    import re

    # Find the [Flaggy] tag and capture everything that follows
    match = re.search(r"\[Flaggy\](.+)", data, re.DOTALL)
    if not match:
        print("No [Flaggy] section found.")
        return

    encoded = match.group(1)
    print(f"Encoded flag content: {encoded}")

    # Decode: for each character, subtract 256 from its code point and convert to a new character
    start = "ddc{"
    # decoded = ''.join(
    #     chr(ord(c) - 256) if ord(c) >= 256 else '?'  # or skip/leave unchanged
    #     for c in encoded
    # )

    # Show the diff from each char to start
    for i in range(len(start)):
        print(f"Char: {start[i]} -> {start[i]}: {ord(start[i]) - ord(encoded[i])}")
    
    return

    # To get the correct flag, we need to add 256 to the code point of each character, but not exactly, so let's try until we get the flag
    adjust = -2000
    decoded = ""
    while True:
        print(f"Trying adjustment: {adjust}")
        try:
            decoded = ''.join(chr(ord(c) + adjust) for c in encoded)
            # print(f"Decoded flag content: {decoded}")
            if decoded.lower().startswith(start):
                break
        except Exception as e:
            pass
        adjust += 1
    
    print("Decoded flag content:")
    print(decoded)


with open("handout/Flaggy_DDC/docProps/core.xml", "r", encoding="utf-8") as file:
    data = file.read()
# Extract the <dc:description> content
# and decode it
dc_description = data.split("<dc:description>")[1].split("</dc:description>")[0]

extract_and_decode_flaggy(dc_description)

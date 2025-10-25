import binascii
import sys

# Constant file header
FILE_HEADER = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"

# Fixed list of possible chunks
PNG_CHUNKS_TYPE = [b"IHDR", b"PLTE", b"IDAT", b"IEND", b"bKGD", b"cHRM", b"dSIG", b"eXIf", b"gAMA", b"hIST", b"iCCP", b"iTXt", b"pHYs", b"sBIT", b"sPLT", b"sRGB", b"sTER", b"tEXt", b"tIME", b"tRNS", b"zTXt"]
SPLITTER = "-----------------------"

def validate_crc(type: bytes, data: bytes, crc: bytes) -> bool:
    """Validate if the CRC is valid given a type and data"""

    print("Validating CRC...")

    c2 = binascii.crc32(type + data)
    
    if c2 == crc:
        print("Valid")
        return True
    else:
        print("Invalid")
        print("Expected :", crc)
        print("Result   :", c2)
        return False

def validate_magicbytes(data) -> int:
    """Validate that the current magicbytes are valid PNG magicbytes"""

    print("Validating magicbytes...")

    magicbytes = data[0 : len(FILE_HEADER)]

    if magicbytes == FILE_HEADER:
        print("Valid")
        return len(FILE_HEADER)
    else:
        print("Invalid")
        print("Expected :", FILE_HEADER)
        print("Result   :", magicbytes)
        return 0

def repair_magicbytes(data: bytes) -> bytes:
    """Set the PNG magicbytes to the correct value"""

    print("Repairing magicbytes")
    
    return FILE_HEADER + data[len(FILE_HEADER):]

def parse_chunks(data: bytes, offset: int):
    """Parse the chunk at a given offset"""

    # First 4 bytes
    chunkLength = data[offset: offset + 4]
    length = int.from_bytes(chunkLength, "big")

    # 4th to 8th bytes
    chunkType = data[offset + 4 : offset + 8]

    # 8th to length bytes
    chunkData = data[offset + 8 : offset + length + 8]
    # length to (length + 4) bytes
    chunkCRC = data[offset + length + 8: offset + length + 12]
    crc = int.from_bytes(chunkCRC, "big")

    print("Parsing header :", chunkType, "at offset", offset + 4, "(", hex(offset + 4), "), with length", length)
    print("CRC :", crc)

    if chunkType not in PNG_CHUNKS_TYPE:
        print("Type is invalid")
        return 0

    if length != len(chunkData):
        print("Length is invalid")
        return -2

    if not validate_crc(chunkType, chunkData, crc): # and chunkType != b"IEND":
        print("CRC is invalid")
        return -1
    
    return offset + 8 + length + 4

def manual_repair_idat(data: bytes, offset: int) -> bytes:
    """Replace the IDAT chunk with a new one"""

    # First 4 bytes
    chunkLength = data[offset: offset + 4]
    length = int.from_bytes(chunkLength, "big")

    # 4th to 8th bytes
    chunkType = data[offset + 4 : offset + 8]
    if chunkType != b"IDAT":
        return data

    # 8th to length bytes
    chunkData = data[offset + 8 : offset + length + 8]
    # length to (length + 4) bytes
    chunkCRC = data[offset + length + 8: offset + length + 12]
    crc = int.from_bytes(chunkCRC, "big")

    print("Parsing header :", chunkType, "at offset", offset + 4, "(", hex(offset + 4), "), with length", length)
    print("CRC :", crc)

    if not validate_crc(chunkType, chunkData, crc):
        print("CRC is invalid")
        # Find offset of next IDAT (or IEND) chunk
        index = data.find(b"IDAT", offset + 8)
        if index == -1:
            index = data.find(b"IEND", offset + 8)
            if index == -1:
                print("No IDAT or IEND found, reverting")
                return data
            else:
                print("Found IEND at offset", index)
        else:
            print("Found IDAT at offset", index)
        
        # Modify the length of the chunk to the diff between the current offset and the next IDAT or IEND
        # also taking into consideration the CRC of the chunk (4 bytes) and the next chunk length (4 bytes)
        # length = index - offset - 8 - 4 - 4
        # chunkLength = length.to_bytes(4, "big")
        # chunkData = data[offset + 8 : offset + length + 8]
        # chunkCRC = data[offset + length + 8: offset + length + 12]
        # crc = int.from_bytes(chunkCRC, "big")
        # print("New length :", length)
        # print("New CRC :", crc)
        # if not validate_crc(chunkType, chunkData, crc):
        #     print("CRC is still invalid...")
        #     # print("Removing chunk")
        #     # return data[:offset] + data[offset + length + 12:]

        # Make the length of the chunk 65524
        length = 65524
        # Cut off excess data (up to CRC and next chunk)
        data = data[:offset + 8 + length + 4] + data[index - 4:]
        # Recalculate the CRC
        chunkLength = length.to_bytes(4, "big")
        chunkData = data[offset + 8 : offset + length + 8]
        chunkCRC = data[offset + length + 8: offset + length + 12]
        crc = int.from_bytes(chunkCRC, "big")
        print("New length :", length)
        print("New CRC :", crc)
        if not validate_crc(chunkType, chunkData, crc):
            print("CRC is still invalid...")
            # print("Removing chunk")
            # return data[:offset] + data[offset + length + 12:]



    # original_length = length
    # length = 1
    # while not validate_crc(chunkType, chunkData, crc):
    #     print(f"CRC is invalid, trying length {length}")
    #     chunkLength = length.to_bytes(4, "big")
    #     chunkData = data[offset + 8 : offset + length + 8]
    #     chunkCRC = data[offset + length + 8: offset + length + 12]
    #     crc = int.from_bytes(chunkCRC, "big")
    #     length += 1
    #     if length > 1000000:
    #         print("Length too long, reverting")
    #         length = original_length
    #         chunkLength = original_length.to_bytes(4, "big")
    #         chunkData = data[offset + 8 : offset + original_length + 8]
    #         chunkCRC = data[offset + original_length + 8: offset + original_length + 12]
    #         break
    
    return data[:offset] + chunkLength + chunkType + chunkData + chunkCRC + data[offset + length + 12:]

def repair_chunk_manual(data: bytes, offset: int) -> bytes:
    """Replace the chunk type for a given chunk"""

    # [Part1 | chunkLength | chunkType | part2]
    part1 = data[:offset]

    # First 4 bytes
    chunkLength = data[offset: offset + 4]
    length = int.from_bytes(chunkLength, "big")

    # 4th to 8th bytes
    chunkType = data[offset + 4 : offset + 8]

    part2 = data[offset + 8:]

    
    print(f"Manual repair, chunk type {chunkType} at offset {offset + 4} ({hex(offset + 4)}) with length {length}")
    if chunkType == b"RHDR":
        # Set chunkLength in data to 13
        length = 13
        chunkType = b"IHDR"
        chunkLength = length.to_bytes(4, "big")
    elif chunkType == b"sRGB" and length != 1:
        length = 1
        chunkLength = length.to_bytes(4, "big")
    elif chunkType == b"MAMA":
        chunkType = b"gAMA"

    # if len(header) != 4:
    #     print("Wrong header type length. Exiting.")
    #     exit(1)

    # Replace the old header by the user-input header
    return part1 + chunkLength + chunkType + part2

def repair_chunk_type(data: bytes, offset: int) -> bytes:
    """Replace the chunk type for a given chunk"""

    # [Part1 | chunktype | part2]
    part1 = data[:offset + 4]
    chunkType = data[offset + 4: offset + 8]
    part2 = data[offset + 8:]

    print("Repairing chunk type")
    print("Current type :", chunkType)
    print("Possible choices :", PNG_CHUNKS_TYPE)

    header = input("Enter the header manually : ").encode()

    # if len(header) != 4:
    #     print("Wrong header type length. Exiting.")
    #     exit(1)

    # Replace the old header by the user-input header
    return part1 + header + part2

def repair_chunk_crc(content: bytes, offset: int) -> bytes:
    """Calculate and replace the CRC for a given chunk"""

    # [Part1 | CRC | part2]    
    chunkLength = content[offset: offset + 4]
    length = int.from_bytes(chunkLength, "big")

    chunkType = content[offset + 4 : offset + 8]
    chunkData = content[offset + 8 : offset + length + 8]

    part1 = content[:offset + length + 8]
    part2 = content[offset + length + 12:]

    print("Repairing chunk CRC (Replacing old CRC by actual CRC)")
    c2 = binascii.crc32(chunkType + chunkData)
    c2 = c2.to_bytes(4, "big")

    print("New CRC :", c2)

    return part1 + c2 + part2

def repair_chunk_length(content: bytes, offset: int) -> bytes:
    """Attempts to repair a chunk's length by crawling for the next type chunk in the data"""

    part1 = content[:offset]
    part2 = content[offset + 4:]
    data = content[offset + 8:]

    index = 99999999999999999
    for t in PNG_CHUNKS_TYPE:
        i = data.find(t)
        if i != -1 and i < index:
            index = i

    print("Found another chunk, resizing...")
    # We need the index before the next chunk, not the next chunk.
    index = index - 8
    index = index.to_bytes(4, "big")

    return part1 + index + part2

def parse_and_repair_magicbytes(content: bytes) -> [bytes, int]:
    """Try to parse the magicbytes and handle the errors"""

    new_offset = validate_magicbytes(content)
    if new_offset == 0:
        content = repair_magicbytes(content)
        print("Retrying...")
        new_offset = validate_magicbytes(content)
    return content, new_offset

def parse_and_repair_chunk(content: bytes, offset: int) -> [bytes, int]:
    """Try to parse one chunk and handle the related errors"""

    content = repair_chunk_manual(content, offset)
    content = manual_repair_idat(content, offset)
    new_offset = parse_chunks(content, offset)

    if new_offset == 0:
        # Invalid type
        content = repair_chunk_type(content, offset)
        print("Retrying...")
        new_offset = parse_chunks(content, offset)
    
    if new_offset == -2:
        # Invalid length
        content = repair_chunk_length(content, offset)
        print("Retrying...")
        new_offset = parse_chunks(content, offset)

    if new_offset == -1:
        # Invalid CRC
        content = repair_chunk_crc(content, offset)
        print("Retrying...")
        new_offset = parse_chunks(content, offset)
    return content, new_offset

def parse():
    """Run the """

    # Validate arguments count
    if len(sys.argv) != 3:
        print("Usage : png_parser.py <input.png> <output.png>")
        exit(0)

    # Dump PNG in a buffer
    content = None
    with open(sys.argv[1], "rb") as f:
        content = f.read()

    content, offset = parse_and_repair_magicbytes(content)
    print(SPLITTER)

    # While the PNG has not been completly parsed
    while offset < len(content):
        content, offset = parse_and_repair_chunk(content, offset)
        print(SPLITTER)

    print("Done fixing, writing output image to", sys.argv[2])

    with open(sys.argv[2], "wb") as f:
        f.write(content)

if __name__ == "__main__":
    parse()
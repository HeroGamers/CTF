pwd_mask = [ 0x70, 0x70, 0x67, 0xb7, 0xfc, 0xc6, 0xa0, 0xce, 0x7b, 0xc8, 0xd4, 0x29, 0x6f, 0x8c, 0x20, 0x6d, 0x5f, 0xeb, 0x78, 0x36, 0xf3, 0xe9, 0xc4, 0xd3, 0x3b, 0x27, 0x2d, 0x46, 0x97, 0xf7, 0xb9, 0xa3, 0x06, 0x3c, 0xc6, 0x0b, 0x3e, 0x75, 0xc6, 0x42, 0x62, 0x87, 0xfc, 0x36, 0xe3, 0x93, 0x8e, 0xa8, 0xcc, 0x24, 0x34, 0x34 ]

output = []
for i in range(200):
    output.append(pwd_mask[i] ^ pwd_mask[3-i])
    print(output)
    for word in output:
        try:
            print(chr(word), end="")
        except:
            pass
    
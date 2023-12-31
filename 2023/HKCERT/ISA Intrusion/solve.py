hex = [
    0xcd98394d,
    0xb3d55b45,
    0xdfcd034a,
    0xa7dd4e9f,
    0xe306c1ea,
    0x7bfba3,
    0xf69fbcc5,
    0x4493b0c7,
    0xf48710fc,
    0x4605c0a1,
    0x7714569d,
    0x99e0ee,
    0x418372ef,
    0x810089a6,
    0xf613a578,
    0x327f241e,
    0x39b92ff4,
    0x3ce1d9c7,
    0x28a53724,
    0xc341fce,
    0x93e9df15,
    0xde0c7383,
    0x161c73a6,
    0x5fed2896,
    0xe302a383,
    0xb18e3a66,
    0x93af8a20,
    0x71426981,
    0x855ec36b,
    0x51b4612d,
    0x7227ddc8,
    0x2f2fbbd6,
    0x63e8c5b,
    0x5ac9e294,
    0xe30baa4b,
    0x8e009a51,
    0x6e5e1eac,
    0x5bed520d,
    0xafac26ce,
    0xa46a180c,
    0x4cf5b158,
    0x148d9fbd,
    0xa008a3c0,
    0x8d4e9273,
    0xb21906e5,
    0xd20edf1,
    0x179f5e2d,
    0xdfcc7b6c,
    0xfdc42107,
    0x1ecbb256,
    0x83e9fcd4,
    0xdf852e9a,
    0x51709534,
    0xdd7c720b,
    0x4d4d5f38,
    0x8da3d994,
    0x264ff8ec,
    0xbd52ff7b,
    0x73ff6db7,
    0x7ffff535,
    0x5feb7f33,
    0xfd3e69ff,
    0xf5b5ff5f,
    0xf57775ff,
    0xfff673fb,
    0xdf777bfd,
    0xf6ef7ff6,
    0x7f36b7ff,
    0x7a377bfb,
    0x75f7fff7,
    0x777fdf3b,
    0x7f7df673,
    0x7f3ff77f,
    0x7ff6f67e,
    0x6777ef6a,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x4161,
    0x50210d13,
    0x48511414,
    0x66b2330,
    0x200021,
    0x6410501d,
    0x50115002,
    0xd060202,
    0x1612029,
    0x104a4924,
    0x43100558,
    0x52104820,
    0x404650,
    0x21204d13,
    0x24205011,
    0x24207331,
    0x11127462,
    0x226a28
]


def solve():
    flag_hex = ''
    for i in range(len(hex)-1, 0, -1):
        # Convert every integer back to hex
        int_as_hex = hex[i].to_bytes(4, 'big').hex()
        flag_hex += int_as_hex
    print(flag_hex)


if __name__ == '__main__':
    solve()

import aiohttp
import asyncio
import json

CHALLENGE = "http://chal.hkcert23.pwnable.hk:28231"
session: aiohttp.ClientSession


async def get_flag():
    async with session.get(f"{CHALLENGE}/encrypt/flag") as resp:
        res = await resp.text()
        print(res)
        json_res = json.loads(res)
        return json_res["ciphertext"]


async def encrypt(message):
    print(f"Encrypting {message}")

    params = {
        "m": message
    }
    async with session.get(f"{CHALLENGE}/encrypt", params=params) as resp:
        res = await resp.text()
        print(res)
        json_res = json.loads(res)
        return json_res["ciphertext"]


async def main():
    global session
    session = aiohttp.ClientSession()

    # We have the entire flag
    flag = await get_flag()

    # Each 8 bytes is a block, and it's in hex so we make it back into ints so we can work with it
    c = [int(flag[i:i + 16], 16) for i in range(0, len(flag), 16)]
    print([hex(i) for i in c])

    m = ''
    for i in range(1, len(c)):
        # by XOR'ing c_i-1 and c_i and encrypting it we get c_i-1 XOR m_i-1 XOR m_i
        print(f"c[{i-1}] ^ c[{i}] = {hex(c[i - 1])} ^ {hex(c[i])} = {hex(c[i - 1] ^ c[i])}")
        to_encrypt = c[i - 1] ^ c[i]
        to_encrypt_hex = hex(to_encrypt)[2:]
        # # We pad it with 0s to make it 8 bytes
        # to_encrypt_hex = '0' * (16 - len(to_encrypt_hex)) + to_encrypt_hex

        encrypted = (await encrypt(m+to_encrypt_hex))[16*i:-16]
        print(f"encrypted = {encrypted}")
        # We XOR the result with c_i-1 to get m_i
        m_i = hex(c[i - 1] ^ int(encrypted, 16))[2:]
        # # pad it with 0s again
        # m_i = '0' * (16 - len(m_i)) + m_i
        m += m_i

        print(f"m[{i}] = {m_i}")
        print(f"m = {m}")
        print(f"m decrypted = {bytes.fromhex(m).decode()}")

    # We have the flag
    print(bytes.fromhex(m).decode())



if __name__ == '__main__':
    asyncio.run(main())
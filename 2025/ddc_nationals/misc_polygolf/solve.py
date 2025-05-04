import asyncio
import json
import aiohttp

URL = "http://localhost:8080/run"

async def exploit():
    async with aiohttp.ClientSession() as session:
        # Create a payload that will trigger the vulnerability
        # challenge = secrets.token_hex(16)
        # expected = long_to_bytes(binascii.crc32(challenge.encode())).hex()
        # The code needs to take the challenge as an argument, and return expected - it needs to be both valid python and js code!
        payload = {
            "code": """
#/*s="challenge";import binascii;print(format(binascii.crc32(s.encode())%2**32,'08x'))#*/console.log(("00000000"+(require("crc-32").str("challenge")>>>0).toString(16)).slice(-8))//*/
            """
        }
        # Make the code smaller, remove any extra whitespaces
        payload["code"] = payload["code"].strip()
        # Send the payload to the server
        async with session.post(URL, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                print("Success:", data)
            else:
                print("Error:", response.status, await response.text())

async def main():
    await exploit()


if __name__ == "__main__":
    asyncio.run(main())
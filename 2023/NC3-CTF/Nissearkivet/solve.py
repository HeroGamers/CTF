import subprocess
import tqdm

wl = ['nisse', 'arkivet', 'nissearkivet', 'nissearkivet123', 'nisse123', 'arkivet123', 'nissearkivet123',
      'nisse123arkivet', 'nisse123arkivet123', 'nissearkivetnisse', 'nissearkivetarkivet', 'nissearkivetnissearkivet',
      'nissearkivetnisse123', 'nissearkivetarkivet123', 'nissearkivetnissearkivet123', 'nissearkivet123nisse',
      'nissearkivet123arkivet', 'nissearkivet123nissearkivet', 'nissearkivet123nisse123', 'nissearkivet123arkivet123',
      'nissearkivet123nissearkivet123', 'arkivetnisse', 'arkivetarkivet', 'arkivetnissearkivet', 'arkivetnisse123',
      'arkivetarkivet123', 'arkivetnissearkivet123', 'arkivet123nisse', 'arkivet123arkivet', 'arkivet123nissearkivet',
      'arkivet123nisse123', 'arkivet123arkivet123', 'arkivet123nissearkivet123', 'nissearkivetnisse',
      'nissearkivetarkivet', 'nissearkivetnissearkivet', 'nissearkivetnisse123', 'nissearkivetarkivet123',
      'nissearkivetnissearkivet123', 'nissearkivet123nisse', 'nissearkivet123arkivet', 'nissearkivet123nissearkivet',
      'nissearkivet123nisse123', 'nissearkivet123arkivet123', 'nissearkivet123nissearkivet123', 'nisse', 'arkivet',
      'nissearkivet', 'nissearkivet123', 'nisse123', 'arkivet123', 'nissearkivet123', 'nisse123arkivet',
      'nisse123arkivet123', 'nissearkivetnisse', 'nissearkivetarkivet', 'nissearkivetnissearkivet',
      'nissearkivetnisse123', 'nissearkivetarkivet123', 'nissearkivetnissearkivet123', 'nissearkivet123nisse',
      'nissearkivet123arkivet', 'nissearkivet123nissearkivet', 'nissearkivet123nisse123', 'nissearkivet123arkivet123',
      'nissearkivet123nissearkivet123', 'arkivetnisse', 'arkivetarkivet', 'arkivetnissearkivet', 'arkivetnisse123',
      'arkivetarkivet123', 'arkivetnissearkivet123', 'arkivet123nisse', 'arkivet123arkivet', 'arkivet123nissearkivet',
      'arkivet123nisse123', 'arkivet123arkivet123', 'arkivet123nissearkivet123']

print("Loading rockyou.txt")
with open("rockyou.txt", encoding='utf-8', errors='ignore') as f:
    wl += f.read().split("\n")
print("Loading dk_breach.txt")
with open("dk_breach.txt", encoding='utf-8', errors='ignore') as f:
    wl += f.read().split("\n")
print("Loading 20200419-Danish-words.txt")
with open("20200419-Danish-words.txt", encoding='utf-8', errors='ignore') as f:
    wl += f.read().split("\n")

print(f"Loaded {len(wl)} passwords")


def test(passwd, f):
    out = subprocess.run(['C:\\Program Files (x86)\\UHARC CMD\\bin\\uharc.exe', 'e', f'-pw{passwd}', f], stdout=subprocess.PIPE)
    return out.returncode, out.stdout


file = 'nissearkivet.uha'
while True:
    for password in tqdm.tqdm(wl):
        # print(f'[Trying] : {password}')
        status, res = test(password, file!)
        if b'ERROR' not in res or status == 0:
            print(f'[Found] : {password}')
            # c += 1
            # os.remove(file)
            # os.rename('nissearkivet', file)
            print(res)
            break

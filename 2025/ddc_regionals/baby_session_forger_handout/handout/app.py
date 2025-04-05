from flask import Flask, request, session
import os

app = Flask(__name__)

secret_hex = "F8 A0 CF 89 9F C7 FF 42 89 72 6D CF D1 68 B7 14 3A DA 0A 31 1F D7 F5 3B 8F B7 2E AC 43 C4 8F C2 CC 7A F5 29 5F 66 C5 B0 57 0F D3 D3 9D 00 D8 70 99 B7 0F E4 B0 05 D1 EB F7 DC 91 9D C2 96 52 36"

# Convert hex string to bytes
secret_bytes = bytes.fromhex(secret_hex.replace(" ", ""))
app.secret_key = secret_bytes #b'\xf5\x9fd\xbd]\xb5q`\xda\xf5\xe8qdV\xbaU\xc4\x1d\xa7\xcb\xebCrX\xb7"\x8eQ\x11\tQ~;lf\xdaj6\xad\xf6\xa7\x94\x8d\xf3Q\xf5\x9e\x08M2O;f\x90E\xce7\xcf~\x1fS\x08\x19E'

@app.route("/")
def index():
    if not 'authed' in session:
        session["authed"] = True
    session["authed"] = True
    return f"Hello, {session['authed']}"

@app.route("/fileread", methods=["POST"])
def fileread():
    if request.method == "POST":
        filename = request.form["filename"]
        offset = request.form["offset"]
        amount = request.form["amount"]

        fullpath = os.path.abspath(filename)

        if not os.path.isfile(fullpath):
            return f"Nope, not a file - {fullpath}"
        if not offset.isdigit():
            return f"Nope, offset not a digit - {offset}"
        if not amount.isdigit():
            return f"Nope, amount not a digit - {amount}"
        if "/app" in fullpath:
            return f"Nope, app - {fullpath}"
        
        amount = int(amount)
        offset = int(offset)
        ret = ""
        with open(filename, "rb") as f:
            f.seek(offset)
            ret = f.read(amount)
        
        return ret

@app.route("/flag")
def flag():
    if session["authed"] == True:
        flag = open("./flag.txt", "r").read()
        return "Here's your flag: " + flag
    return "Naaaaa"
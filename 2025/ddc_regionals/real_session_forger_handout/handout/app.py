from flask import Flask, request, session
import os

app = Flask(__name__)

app.secret_key = os.urandom(64)

@app.route("/")
def index():
    if not 'authed' in session:
        session["authed"] = False
    return ":)"

@app.route("/fileread", methods=["POST"])
def fileread():
    if request.method == "POST":
        filename = request.form["filename"]
        offset = request.form["offset"]
        amount = request.form["amount"]

        fullpath = os.path.realpath(filename)

        if not os.path.isfile(fullpath):
            return "Nope"
        if not offset.isdigit():
            return "Nope"
        if not amount.isdigit():
            return "Nope"
        if "/app" in fullpath:
            return "Nope"
        
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
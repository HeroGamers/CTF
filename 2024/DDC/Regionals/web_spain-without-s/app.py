from flask import Flask, render_template, request, make_response, redirect
from db import query_users
from util import merge, valid_filename
import json
from util import verify_jwt, valid_filename, check_secret_key, create_cookie

app = Flask(__name__)
app.secret_key = "REDACTED" # Not default value :)

# Maybe I should implement this class
class Config:
    def __init__(self):
        pass

@app.route("/update", methods=["GET", "POST"])
def update():
    cookie_value = request.cookies.get("session", "default_value")

    if request.method == "GET":
        if verify_jwt(cookie_value, app.secret_key, check_admin=False):
            return render_template("update.html")
        return render_template("index.html")
    if request.method == "POST":
        if verify_jwt(cookie_value, app.secret_key, check_admin=False):
            data = json.loads(request.data)
            config = Config()
            merge(data, config)

        return "Success", 201

@app.route("/", methods=["GET", "POST"])
def index():
    cookie_value = request.cookies.get("session", "default_value")

    if request.method == "GET":
        if verify_jwt(cookie_value, app.secret_key, check_admin=True):
            return render_template("index_admin.html")
        else:
            return render_template("index.html", secret=app.secret_key)
    else:
        if verify_jwt(cookie_value, app.secret_key, check_admin=True):
            filename = request.form.get("file")

            if valid_filename(filename, allowed_path="/home/bruhbruh/"):
                    try:
                        with open(filename, "r") as f:
                            file_content = f.read()
                    except:
                        return render_template("index_admin.html", content="No such file!")
                    
                    return render_template("index_admin.html", content=file_content)
            else:
                return render_template("index_admin.html", content="You can't see this file :)")
        else:
            return 0
        
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        secretkey = request.form.get("secretkey")

        if query_users(username, password) and check_secret_key(secretkey):
            jwt_token = create_cookie(username, password, jwt_secret=app.secret_key)

            resp = make_response(redirect("/"))
            resp.set_cookie("session", jwt_token)

            return resp
        else:
            return render_template("login.html")

def main():
    app.run(host="0.0.0.0", port=80, debug=False)

if __name__ == "__main__":
    main()
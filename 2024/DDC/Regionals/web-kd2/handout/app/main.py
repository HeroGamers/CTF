from flask import Flask, request, Response, render_template_string, session
import json, os

app = Flask(__name__)
print("started")
# Util stuff
def readfile(path):
    return open(path, "r").read()

def get_query(request):
    query = {}
    query.update(request.args)
    query.update(request.form)
    return query

# Load data
try:
    FLAG = readfile("flag.txt")
except:
    FLAG = "DDC{LOCALFLAG}"
    
try:
    app.config["SECRET_KEY"] = json.loads(readfile("config.json"))["SECRET_KEY"]
except:
    app.config["SECRET_KEY"] = os.urandom(32).hex()


# Please no leak my flag
def is_flag(path,flag):
    # avoid shenanigans
    return (os.path.exists(os.path.abspath(path)) or os.path.exists(os.path.join(os.getcwd(),path))) and flag in readfile(path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'account_type' in session:
        privilige = session["account_type"]
    else:
        session["account_type"] = "USER"
        privilige = "USER"


    requested = get_query(request).get('post', 'index.txt')
    path = os.path.join("posts", requested)

    if not privilige == "ADMIN":
        if is_flag(path,FLAG):
            return "ERROR: that's not one of my posts, stop that!"
    
    text = readfile(path)
    
    return render_template_string(readfile('page.html'), path=path, text=text)
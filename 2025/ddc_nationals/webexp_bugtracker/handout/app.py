import datetime
import json
import secrets
from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt
from jwcrypto import jwk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


SKEY = b"""redacted"""

KEY = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu312Aqc7m8puqI5i0mm4
+CdBRYRmccFwJme1qHVAc0RcIPSS6k3hJ/WZJgQyDuTt/DUtYb2pbVTzIso3v5HR
FodZ8zZdqHLBF+V8uVluwXGyjw5i7mpBS8PJQMMIL3tEPmYB21KKF1cfkMbDYE6S
r8BchYraXnAtLj+w6w1rzTOEYsqbktCq29xXTWU8+E+mOUYKHS8n8olyPEBfiaHY
fy7nUt+uMrUXxayrTWMi7HduFq4ZW7kUnH66koTo26x+HuhHuh9lhIdVLKmB64Yq
Kyt88r1XOAXI9cMVQZqdRuGbYSg8UgLE1mzqxkAzv0E6hITTJYQdCTAiuUX1Dj1M
bwIDAQAB
-----END PUBLIC KEY-----"""

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(32)

client = MongoClient("mongodb://localhost:27017")
tracker_db = client["tracker_db"]
bugs_collection = tracker_db["bugs"]
flags_collection = tracker_db["flags"]
users_collection = tracker_db["users"]


def init_db():
    bugs_collection.delete_many({})
    flags_collection.delete_many({})
    users_collection.delete_many({})

    bugs_collection.create_index([('title', 'text'), ('description', 'text')])

    bugs_collection.insert_many([
        {"title": "Login form error", "description": "Crashes on special characters", "severity": "high", "status": "open"},
        {"title": "CSS misalignment", "description": "Footer overlaps main content", "severity": "low", "status": "open"},
        {"title": "Performance regression", "description": "Page load slow after last update", "severity": "medium", "status": "open"},
    ])

    flags_collection.insert_one({
        "label": "ctf_flag",
        "flag": "DDC{fake-flag}"
    })

    users_collection.insert_one({
        "username": "admin_user",
        "password": secrets.token_hex(32),
        "role": "admin"
    })


def generate_jwt(username, role, algorithm="RS256"):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    if algorithm == "RS256":
        token = jwt.encode(
            payload,
            SKEY,
            algorithm="RS256"
        )
    elif algorithm == "HS256":
        token = jwt.encode(
            payload,
            SKEY,
            algorithm="HS256"
        )
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    return token


def decode_jwt(token):
    header = jwt.get_unverified_header(token)
    alg = header.get("alg")

    if alg == "HS256":
        key_obj = serialization.load_pem_public_key(
            KEY,
            backend=default_backend()
        )
        raw_key_bytes = key_obj.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return jwt.decode(
            token,
            key=raw_key_bytes,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
    elif alg == "RS256":
        return jwt.decode(
            token,
            key=KEY,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
    else:
        raise ValueError(f"Unsupported alg: {alg}")


def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/.well-known/jwks.json')
def jwks():
    key = jwk.JWK.from_pem(KEY)
    return jsonify(key.export_public(as_dict=True))


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/submit_bug")
def submit_bug_page():
    return render_template("submit_bug.html")


@app.route("/admin")
def admin_panel():
    return render_template("admin.html")


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    existing = users_collection.find_one({"username": username})
    if existing:
        return jsonify({"error": "Username already exists"}), 400

    users_collection.insert_one({
        "username": username,
        "password": password,
        "role": "user"
    })
    return jsonify({"success": True, "message": "Account created."})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = users_collection.find_one({"username": username, "password": password})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_jwt(user["username"], user["role"])
    return jsonify({"token": token})


@app.route("/create_bug", methods=["POST"])
def create_bug():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"error": "Missing token"}), 401

    token = auth.split()[1]
    try:
        claims = decode_jwt(token)
    except Exception as e:
        return jsonify({"error": f"Invalid token: {str(e)}"}), 401

    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    severity = data.get("severity", "low")

    if not title or not description:
        return jsonify({"error": "title and description required"}), 400

    bug = {
        "title": title,
        "description": description,
        "severity": severity,
        "status": "open"
    }
    bugs_collection.insert_one(bug)
    return jsonify({"success": True, "message": "Bug created."})


@app.route("/admin_search", methods=["GET"])
def admin_search():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split()[1]
    try:
        claims = decode_jwt(token)
    except Exception as e:
        return jsonify({"error": f"Invalid token: {str(e)}"}), 401

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin privileges required"}), 403

    query_param = request.args.get("query", '[{"$match": {}}]')
    try:
        query = json.loads(query_param)
        if not isinstance(query, list):
            return jsonify({"error": "query must be a JSON array"}), 400
    except:
        return jsonify({"error": "Invalid query JSON"}), 400

    results = list(bugs_collection.aggregate(query))
    return jsonify({"results": convert_objectid_to_str(results)})


init_db()

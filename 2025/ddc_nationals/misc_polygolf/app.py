from flask import Flask, request, jsonify, render_template
from Crypto.Util.number import long_to_bytes 
import subprocess
import tempfile
import secrets
import binascii
import os 
import logging

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "flag{this_is_a_fake_flag_for_testing_purposes}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_js():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    if len(code)>211 or not code.isascii():
        return jsonify({"error": f"Bad program: {len(code)} - {code.isascii()}"}), 401

    with tempfile.NamedTemporaryFile(mode='w') as tmp:
        os.chmod(tmp.name, 0o644)
        challenge = secrets.token_hex(16)
        logging.warning(f"chall: {challenge}")
        expected = long_to_bytes(binascii.crc32(challenge.encode())).hex()
        logging.warning(f"expected: {expected}")
        tmp.write(code)
        tmp.flush()
        try:
            result = subprocess.run(["deno", "run", "--cached-only", tmp.name, challenge], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            logging.warning(f"js result: {output}")
            if result.returncode != 0 or output != expected:
                return jsonify({"error": f"Bad program: {output} != {expected}"}), 401
            
            result = subprocess.run(["python3", tmp.name, challenge], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            logging.warning(f"py result: {output}")
            if result.returncode != 0 or output != expected:
                return jsonify({"error": f"Bad program: {output} != {expected}"}), 401
            
            return jsonify({"success": FLAG}), 200
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

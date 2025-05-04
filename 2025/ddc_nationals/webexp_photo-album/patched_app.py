import os
import tarfile
import secrets
from flask import Flask, request, render_template, send_from_directory, abort

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
EXTRACT_FOLDER = "./static/albums"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_TAR = {".tar"}


def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS or ext.lower() in ALLOWED_TAR


def has_only_images_in_tar(tar_path):
    try:
        with tarfile.open(tar_path, "r") as tar_ref:
            for member in tar_ref.getmembers():
                _, ext = os.path.splitext(member.name)
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    return False
        return True
    except Exception:
        return False


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded!", 400

        file = request.files["file"]
        if not allowed_file(file.filename):
            return "📸 Sorry, this isn't a file-sharing site for random files. **JPEGs, PNGs, or TARs with images only!** 🛑", 400

        file_ext = os.path.splitext(file.filename)[1].lower()
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if file_ext == ".tar":
            if not has_only_images_in_tar(file_path):
                os.remove(file_path)
                return "🤔 Hmmm... This doesn't look like an image. Try again with something *less suspicious*... 👀", 400

            try:
                with tarfile.open(file_path, "r") as tar_ref:
                    tar_ref.extractall(EXTRACT_FOLDER)
                return render_template("success.html")
            except Exception as e:
                return f"Extraction failed: {str(e)}", 500
        else:
            os.rename(file_path, os.path.join(EXTRACT_FOLDER, file.filename))
            return render_template("success.html")
    return render_template("index.html")


@app.route("/gallery")
def view_gallery():
    images = os.listdir(EXTRACT_FOLDER)
    return render_template("gallery.html", images=images)


@app.route("/static/albums/<path:filename>")
def serve_image(filename):
    return send_from_directory(EXTRACT_FOLDER, filename)


@app.route("/flag")
def get_flag():
    # Get the flag from "/flag.txt"
    try:
        with open("/flag.txt", "r") as f:
            flag = f.read()
        return flag
    except Exception as e:
        return f"Error reading flag: {str(e)}", 500
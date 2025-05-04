import subprocess
import os
import pathlib

def uncompress_templeos_filesystem(root_dir: pathlib.Path):
    """
    Uncompress the TempleOS filesystem using the binary from the "templestuff" directory called "tosdeflate",
    which, given the path to a compressed TempleOS file, will uncompress it and output the uncompressed file to stdout.
    """
    # Get the path to the tosdeflate binary
    tosdeflate = pathlib.Path("templestuff/tosdeflate")
    # Check if the tosdeflate binary exists
    if not tosdeflate.exists():
        print(f"tosdeflate not found: {tosdeflate}")
        return
    # Iterate over the files in the root directory
    for file in root_dir.rglob("*"):
        # Check if the file is a regular file
        if file.is_file():
            # Check if the file is a compressed TempleOS file
            if file.suffix == ".Z":
                # Uncompress the file
                output = subprocess.check_output([str(tosdeflate), str(file)])
                # Get the path to the uncompressed file
                uncompressed_file = file.with_suffix("")
                # Write the uncompressed file to disk
                with open(uncompressed_file, "wb") as f:
                    f.write(output)
                print(f"Uncompressed: {uncompressed_file} ({file})")
    print("Done.")

def main():
    # Get the filesystem path
    root_dir = pathlib.Path("filesystem")
    # Check if the filesystem exists
    if not root_dir.exists():
        print(f"Filesystem not found: {root_dir}")
        return
    # Uncompress the filesystem
    uncompress_templeos_filesystem(root_dir)

if __name__ == '__main__':
    # Change the current working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

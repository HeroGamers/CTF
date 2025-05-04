import os
import pathlib

# Change dir to current script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Open GodBible.HC
with open("filesystem/Adam/God/GodBible.HC", "r") as f:
    # Read the content of the file
    content = f.read()
    line_numbers = content.split('DefineLstLoad("ST_BIBLE_BOOK_LINES",')[1].split(');')[0].replace("\n","").split('\\0')
    line_numbers = [line_number.replace(" ", "").replace('"',"").strip() for line_number in line_numbers]
    line_numbers = [int(line_number) for line_number in line_numbers if line_number]
    print(line_numbers)

# Get lines for line numbers matching line from Bible.TXT
with open("filesystem/Misc/Bible.TXT", "r") as f:
    # Read the content of the file
    content = f.read()
    lines = content.split('\n')
    for line_number in line_numbers:
        print(f"{line_number}: {lines[line_number-1]}")

print("Done.")
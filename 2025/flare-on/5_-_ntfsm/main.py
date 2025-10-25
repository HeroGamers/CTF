import os
from pathlib import Path

def unique_strings(strings_file: Path):
    with open(strings_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    print(f"Total lines read: {len(lines)}")
    # Get unique lines, but in the order they first appeared
    seen = set()
    unique_lines = []
    for line in lines:
        line = line.strip()
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    return unique_lines


def analyze_strings():
    strings_file = Path("ntfsm_strings.txt")
    if not strings_file.exists():
        print(f"File {strings_file} does not exist.")
        return

    unique_lines = unique_strings(strings_file)
    print(f"Number of unique strings: {len(unique_lines)}")

    with open("ntfsm_unique_strings.txt", "w", encoding="utf-8") as f:
        for line in unique_lines:
            f.write(line + "\n")

def main():
    analyze_strings()
    

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
import re


def get_muls(memory: str):
    return [mul for mul in re.findall(r"(mul\((\d+),(\d+)\))?(do\(\))?(don't\(\))?", memory) if mul and (mul[0] or mul[3] or mul[4])]

def main():
    with open("03-Mull-It-Over.txt") as f:
        file = f.read()
    
    print(part_1(file))
    print(part_2(file))
    

def part_1(file):
    muls = get_muls(file)
    result = sum([int(mul[1]) * int(mul[2]) for mul in muls if mul[0]])
    return result


def part_2(file):
    muls = get_muls(file)
    do = True
    result = 0
    for mul in muls:
        if do and mul[0]:
            result += int(mul[1]) * int(mul[2])
        if mul[3]:
            do = True
        if mul[4]:
            do = False
    return result




if __name__ == "__main__":
    main()

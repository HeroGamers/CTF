def main():
    with open("01-Historian-Hysteria.txt") as f:
        file_lines = f.readlines()
    list_1 = []
    list_2 = []
    for line in file_lines:
        numbers = [int(number) for number in line.split("   ") if line and "   " in line]
        list_1.append(numbers[0])
        list_2.append(numbers[1])
    
    part_1(list_1.copy(), list_2.copy())
    part_2(list_1, list_2)

    

def part_1(list_1: list, list_2: list):
    # sort the two lists
    list_1.sort()
    list_2.sort()
    # Compute distances
    total_sum = 0
    for i in range(len(list_1)):
        total_sum += abs(list_1[i] - list_2[i])
    print(total_sum)


def part_2(list_1: list, list_2: list):
    appear_count = {}
    for num in list_2:
        if not num in appear_count:
            appear_count[num] = 0
        appear_count[num] += 1
    
    similarity_score = 0
    for num in list_1:
        if num in appear_count:
            similarity_score += num * appear_count[num]
    
    print(similarity_score)


if __name__ == "__main__":
    main()

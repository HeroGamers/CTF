SPECIAL_CHARS = "^&_=\,.#$!+-@*>[</}{:])("
cjilegbdfahmkn = "cjilegbdfahmkn"


def process_input(input_string):
    string_1 = [0] * 4096
    word_122C0 = [0] * 512
    word_E2C2 = [0] * 8192
    number_of_special_chars = 0
    i = 0

    print(len(input_string))

    # Iterate through each character in the input string
    for i, char in enumerate(input_string):
        special_char = SPECIAL_CHARS[ord(cjilegbdfahmkn[ord(char) - 48]) - 87]
        print(f"i: {i}")
        print(f"char: {char}")
        print(f"special_char: {special_char}")
        print(f"number_of_special_chars: {number_of_special_chars}")
        print(f"word_122C0: {''.join([str(x) for x in word_122C0])}")
        print(f"word_E2C2: {''.join([str(x) for x in word_E2C2])}")
        print(f"string_1: {''.join([str(x) for x in string_1])}")

        # Check if the special character is '}'
        if special_char == '}':
            string_1[2 * i] = 7
            # Check if the number of special characters has reached the limit
            if number_of_special_chars == 512:
                print("Error, too many special chars!")
                return 1
            word_122C0[number_of_special_chars] = i
            number_of_special_chars += 1
        else:
            # Check if the special character is within the valid range
            if '*' <= special_char <= '}' and special_char != '{':
                # Map special characters to their corresponding values
                if special_char == '*':  # '*'
                    string_1[2 * i] = 4
                elif special_char == '+':  # '+'
                    string_1[2 * i] = 1
                elif special_char == '-':  # '-'
                    string_1[2 * i] = 2
                elif special_char == '<':  # '<'
                    string_1[2 * i] = 6
                elif special_char == '>':  # '>'
                    string_1[2 * i] = 5
                elif special_char == '@':  # '@'
                    string_1[2 * i] = 3
            else:
                # Invalid special character encountered
                print("Error, invalid char!")
                return 1

    # Check if the number of special characters is non-zero or if i has reached the limit
    print(f"number_of_special_chars: {number_of_special_chars}")
    print(f"i: {i}")
    if number_of_special_chars > 0 or i == 4095:
        return 1

    string_1[2 * i] = 0
    return 0


def func_2(output):
    v1 = [0] * 65536

    for i in range(65536):
        v1[i] = 0

    # Check if output is 42, if true, update output to a specific value
    if output == 42:
        output = -252645158

    return output


# Sample usage
input_string = (
        "77277777906198000000877777777777800000082777779061982790006197780" +
        "00000008777777778000000008772790006198000000827779061977778777780" +
        "00008972777779061980000002790061987777777778777777877778000000000" +
        "00008777777777778000000000000087777777897277790619897277777906190" +
        "80000080000000000008277790000061980027900061980089727779061977789" +
        "72777779061987772790061978727900000061908002790061908027777790061" +
        "97800000008972777906198772777906197778777777777777777827779061980" +
        "08778000000008900000000008"
)
output = process_input(input_string)
if output == 1:
    output = func_2(output)
else:
    print("Error!")
print(output)

import os
import pathlib
import re
import json
from alphabet_mappings import alphabet_mappings

replace_dict = {
    "&nbsp;": " ",
    "&thinsp;": "1",
    "&hairsp;": "0",
}

def main():
    # Read gremlingram.html
    with open("gremlingram.html", "r") as f:
        html = f.read()
    
    # get each "<div class="col-10">...</div>" contents
    divs = re.findall(r'<div class="col-10">(.*?)</div>', html, re.DOTALL)
    #print(f"Found {len(divs)} divs")
    # For each div, get all the html unicode like &thinsp; &nbsp; etc
    contents = ["".join(re.findall(r'&\w+;', div)).strip() for div in divs]
    contents = [content for content in contents if content]
    # Replace the unicode with the corresponding character
    for key, value in replace_dict.items():
        contents = [content.replace(key, value) for content in contents]
    contents = [content.strip() for content in contents]

    # count how many words at different lengths
    word_count = {}
    for content in contents:
        for word in content.split(" "):
            word_count[len(word)] = word_count.get(len(word), 0) + 1
    #print(word_count)

    # We now have binary, pad each word in each string to 8 bits
    contents = [["0"*(8-len(word))+word for word in content.split(" ")] for content in contents]
    # Convert binary to ascii
    #print("\n\n".join([" ".join(content) for content in contents]))

    # get frequency of each word
    freq_dict = {}
    for content in contents:
        for word in content:
            freq_dict[word] = freq_dict.get(word, 0) + 1
    # sort by frequency
    freq_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    #print(freq_dict)
    #print(f"Found {len(freq_dict)} unique words")

    # How many words with more than 2 occurences
    #print(len([word for word, freq in freq_dict.items() if freq > 2]))  # it's 26

    # Use frequency to map to the alphabet
    freq_list = list(freq_dict.keys())
    alphabet = " etaonrishdlfcmugypwbvkjxzqETAONRISHDLFCMUGYPWBVKJXZQ0123456789{}"
    # CUT alphabet to the length of freq_list
    alphabet = alphabet[:len(freq_list)]
    # alphabet_mappings = {alphabet[i]: alphabet[i] for i in range(len(alphabet))}
    # # save alphabet to file
    # with open("alphabet.json", "w", encoding="utf8") as f:
    #     f.write(json.dumps(alphabet_mappings, ensure_ascii=False, indent=4))

    freq_to_alphabet = {freq_list[i]: alphabet[i] for i in range(len(alphabet))}
    #print(freq_to_alphabet)
    # load freq_to_alphabet from file

    # Replace the binary with the alphabet
    contents = [[freq_to_alphabet[word] for word in content if word in freq_to_alphabet] for content in contents]
    output = "\n\n".join(["".join(content) for content in contents])
    print(output)

    # apply substitution
    new_output = ""
    for char in output:
        new_output += alphabet_mappings.get(char, char)
    print(new_output)

    # Get a mapping of the alphabet to the original binary
    alphabet_to_freq = {alphabet_mappings.get(v, v): k for k, v in freq_to_alphabet.items()}
    #print(alphabet_to_freq)

    # Sort alphabet_to_freq by key
    alphabet_to_freq = dict(sorted(alphabet_to_freq.items(), key=lambda item: item[0]))
    
    # # Revert the keys and values in alphabet_to_freq
    freq_to_alphabet = {v: k for k, v in alphabet_to_freq.items()}
    # # Sort by keys
    freq_to_alphabet = dict(sorted(freq_to_alphabet.items(), key=lambda item: item[0]))

    
    with open("freq_to_alphabet.json", "r", encoding="utf8") as f:
        other_freq_to_alphabet = json.load(f)
    
    # compare and print the differences
    for k, v in freq_to_alphabet.items():
        if other_freq_to_alphabet.get(k, None) != v:
            print(f"{k}: {other_freq_to_alphabet.get(k, None)} -> {v}")

    # print(freq_to_alphabet)
    # with open("freq_to_alphabet.json", "w", encoding="utf8") as f:
    #     f.write(json.dumps(freq_to_alphabet, ensure_ascii=False, indent=4))
    
    # contents = [[freq_to_alphabet[word] for word in content if word in freq_to_alphabet] for content in contents]
    # output = "\n\n".join(["".join(content) for content in contents])
    # print(output)
    
    # use the new freq_to_alphabet to make the correct output
    # new_output = ""
    # for char in output:
    #     new_output += freq_to_alphabet.get(char, char)
    # print(new_output)


    # write output in utf8 to file
    with open("output.txt", "w", encoding="utf8") as f:
        f.write(new_output)


if __name__ == "__main__":
    # Set current working directory to the location of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()
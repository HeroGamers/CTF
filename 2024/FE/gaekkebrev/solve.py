from arrays import *
import numpy as np

print(f"{del1Braille=}\n{del2Braille=}\n{keyBraille=}\n{keyBrailleRow1Total=}\n{keyBrailleRow2Total=}\n{keyBrailleRow3Total=}")
print(f"{braile_dict=}")

def del1_solve():
    del1 = []
    for word in del1Braille:
        word_arr = []
        for letter in word:
            for key, value in braile_dict.items():
                if letter == value:
                    word_arr.append(key)
                    break
            else:
                word_arr.append("?")
        del1.append("".join(word_arr))
    
    print(f"Del 1: {' '.join(del1)}")

del1_solve()

def get_key():
    # bruteforce time
    while True:
        keyBrailleRow1 = 3
        keyBrailleRow2 = 1
        keyBrailleRow3 = 1


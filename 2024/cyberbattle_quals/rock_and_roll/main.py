# load the file
with open("rock_and_roll/ROCK_AND_ROLL-lyrics.txt", "r") as file:
    lyrics = file.read()

# for each non-empty line in the file count the number of words
words_count = [len(line.split()) for line in lyrics.split("\n") if line]
print(words_count)
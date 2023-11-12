import base64
import os
from io import BytesIO
import random
from PIL import Image

all_data = b""

files = os.listdir("../trash")
sorted_files = sorted(files, key=lambda x: int(x, 16))

files_with_data = {}
starts = {}
ends = {}

matches = {"3d19": ["9a2a", "3c99", "bce0", "ec68"],  # end 56af (also works with this order: 3c99-bce0-ec68-9a2a)
           "931b": ["2450", "9af1", "e8e7"],  # end a577 (instead of 2ab4 you can use 122d, 980a or b52d)
           "2857": ["7136", "5849", "6721", "17de"],  # end 361d and 914a
           "8889": ["2373", "cbc8", "2abb"],  # end 914a/8d9b (works with b52d, 122d)
           "bf65": ["25ad", "7960", "b52d"],
           "ce26": ["1934", "628d", "9f93", "27f5"]}  # end 914a/8d9b

all_taken_matches = [match for matches in matches.values() for match in matches]

for filename in sorted_files:
    new_name = int(filename, 16)
    print(f"Opening {filename} -> {new_name}", end="")
    with open("trash/"+filename, "rb") as file:
        base64_data = file.read()
        decoded_data = base64.b64decode(base64_data)

        if b'\xff\xd8' in decoded_data:
            print(": Start Of Image!", end="")
            starts[filename] = decoded_data
        elif b'\xff\xd9' in decoded_data:
            print(": End Of Image!", end="")
            ends[filename] = decoded_data
        elif b'\xff\xc2' in decoded_data:
            print(": Start Of Frame!", end="")
        else:
            files_with_data[filename] = decoded_data

for start, start_data in starts.items():
    print("=====================================")
    print(f"Running for start: {start}")
    print("=====================================")
    # file_data = random.sample(list(files_with_data.items()), 4)
    end, end_data = random.choice(list(ends.items()))
    start_matches = matches[start[:4]]
    matches_data = [data for file, data in files_with_data.items() if file[:4] in start_matches]
    for file, file_data in files_with_data.copy().items():
        if file[:4] in all_taken_matches:
            continue

        data_items = matches_data + [file_data] * (4 - len(matches_data))
        data_names = [filename[:4] for filename in start_matches] + [file[:4]] * (4 - len(matches_data))

        for i in range(0, 10):
            combination = random.sample(range(0, 4), 4)
            # if end not in ends:
            #     break
            # image_data = start_data + file_data[0][1] + file_data[1][1] + file_data[2][1] + file_data[3][1] + end_data
            # name = f"{start[:4]}-{file_data[0][0][:4]}-{file_data[1][0][:4]}-{file_data[2][0][:4]}-{file_data[3][0][:4]}-{end[:4]}"
            image_data = start_data + data_items[combination[0]] + data_items[combination[1]] + data_items[combination[2]] + data_items[combination[3]] + end_data
            name = f"{start[:4]}-{data_names[combination[0]]}-{data_names[combination[1]]}-{data_names[combination[2]]}-{data_names[combination[3]]}-{end[:4]}"

            try:
                image = BytesIO(image_data)
                img = Image.open(image)
                if img.format == "JPEG":
                    img.verify()
                    img.close()
                    img = Image.open(image)
                    img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.close()
                    print(f"Valid image! - {name}")
                    with open(f"convertedtrash/{name}.jpeg", "wb") as file:
                        file.write(image_data)
                    # ends.pop(end)
                    # files_with_data.pop(file_with_data_1)
                    # files_with_data.pop(file_with_data_2)
                    # files_with_data.pop(file_with_data_3)
                    # files_with_data.pop(file_with_data_4)
                else:
                    pass
                    # print(f"Not valid image! - {name}")
            except Exception as e:
                pass
                # print(f"Not valid image! - {name} | Error: {e}")

with open("help.jpeg", "wb") as helpfile:
    helpfile.write(all_data)

import os
import random
from PIL import Image
from pathlib import Path

köttbullar_dir = "./assets/köttbullar"
hotdogs_dir = "./assets/hotdogs"
output_dir = "./encoded"


def encrypt_flag():
    os.makedirs(output_dir, exist_ok=True)
    köttbullar_files = [
        os.path.join(köttbullar_dir, f) for f in os.listdir(köttbullar_dir)
    ]
    hotdogs_files = [os.path.join(hotdogs_dir, f) for f in os.listdir(hotdogs_dir)]

    with open("./secret.txt", "r") as f:
        FLAG = f.read().strip()

    bin_str = "".join(format(ord(c), "08b") for c in FLAG)

    for i, bit in enumerate(bin_str):
        src = (
            random.choice(köttbullar_files)
            if bit == "0"
            else random.choice(hotdogs_files)
        )
        dst = os.path.join(output_dir, f"{i:04}.jpeg")
        with Image.open(src) as img:
            img.save(dst, format="JPEG", quality=95)

    print(f"Encoded {len(bin_str)} bits with CODEBULLAR encoding")

file_hashes = {}


classification_map = {
    "0d35fab55fc4abcb980ff7b008adfc2176bf56a6b50f7377480e6e566d69082d": "hotdog",
    "17ed9e347d9f373a95a3cd467aaa83ef5ee1bb756b3171b542b349a4d8ded6e0": "hotdog",
    "18570beaa182db171fbcf060c312ba0b899e44335ad251ed3ab1d9118ab10067": "hotdog",
    "201d25acfc6afd7ba6b7d1bc855668fa49a5f81c8e30dcbb6879a55acda52c5a": "köttbullar",
    "2f372f5bc5eb78bad4b45166e4d50ce90a98ca9a96f9028a18c895045f330c52": "köttbullar",
    "328c4e1bc30130e40e546b4078684c6da01be51ff0adc00b60d9fe2cf36204d9": "hotdog",
    "3dcec7423f045bbb6f50dd1d2c7a2c2621f3b7e9d57224ec4ad44bbbb7e9aa0f": "hotdog",
    "45070b30ec75aafec31c482efd0c2dd8b9c478998846fbcb00342c78830baec2": "köttbullar",
    "56cf84031a7ce0a53924965e4b81e9a2ed5f0e1ddde6f8fc4f8a86434cd92786": "hotdog",
    "5915f8bb2fa701346b97ce963f7b28b0d4d090ca2d0ed2271f9b5f50bc015562": "köttbullar",
    "59c76b5732491164bb8a0bbe3fa71af7de0467fdf5c115c14d8a0d11ba32a453": "hotdog",
    "764317e06eed17e9afabb0ca0aefcb472e142aa0522e61cfc080fb85288b80f7": "hotdog",
    "81370bff7e0a4ebeb57dc1c287ae8254df8a99a267fd73de1522ad4da1d05bac": "köttbullar",
    "9073b8eca91828bbec9fee2833216d8c3d656d4034ce0ed458644a76e2494d62": "köttbullar",
    "931a3603592118cb52ee1f1dbcb90d993331352b9f90a40ccdd71d4f18f1fcc3": "köttbullar",
    "99121e5499509150d1204612706aa8bcd668e17d37a094d7d5ad1bfefe9b6e91": "köttbullar",
    "9aaf30c8d871117c2cbd35e76b31e5469f0613c1d1f15f0d458e9c41dad854e8": "hotdog",
    "a043934e56d31c955f63a82405a130b06e76f80b966e7881b9410c30f795a3bc": "köttbullar",
    "a42c5edf01b842fdbd208ed6b8ded777c440ab07ca3a3feed3ff7e2ad20ddfa9": "hotdog",
    "a7f8645997b5c7aeeb2f033ca38cc2b7f0aaf197374557aafb6f99dfb5fac044": "hotdog",
    "a9696411518528913ce38d000b6563b8169ec222fbf3d136c72b356167132d34": "köttbullar",
    "ab858b4bc243616a1c0c10059c254c7caab3d381bf346c63e0797b2110f2c798": "hotdog",
    "ae1a30f204eb821a7cc53271d39e75952dda73635b00a7aca17e9384b854475e": "köttbullar",
    "b8329427d2f594e6e6ef1dee9e7d7c00795c1267ff369148603cd282076d8410": "köttbullar",
    "bdbb5431734f277a1dd078eb8d7ef81f3f4d47e04b047de651b30e7f360a7485": "köttbullar",
    "c90fbb088137153c61a3e7eac5befc6049aa9b8ffa53d5b8f6f387e024d506a7": "köttbullar",
    "d38e37955e307e2a760237d26011d4301e92e89e381a12ed6c64b798acccda74": "hotdog",
    "d41143ea7b9538216d4e36733d9e9711e50c435f3e5870ee128743876de8bac9": "hotdog",
    "d9eb41959574edaa3d94983e263508e6e91351afc5c1e7368231dcb58fb148b6": "hotdog",
    "df7d52efe315d09042ec4047accae7555431df57c1eb3d0bda9a068ffbdf5fbb": "köttbullar",
    "f2a40225b79c32fec55b93897534fc78da19870d9fcc5d0e40794e178f78b69e": "köttbullar",
    "fcdf1fadadbba31289e3d5512bdec91d3183e56465b300e53328656721867846": "hotdog",
}

def classify_images():
    # Get amount of files in output_dir
    num_files = len(os.listdir(output_dir))
    print(f"Classifying {num_files} images...")
    # Read sha256sum output
    with open("./sums", "r") as f:
        sha256sum = f.read().strip()
    sha256sums = sha256sum.splitlines()
    print(f"Checksum count: {len(sha256sums)}")

    assets_dir = "./assets"
    unique_hashes = set()
    hashes = {}
    for line in sha256sums:
        hash_value, filename = line.split()
        file_hashes[filename] = hash_value
        if hash_value not in unique_hashes:
            with open(os.path.join(assets_dir, f"{hash_value}.jpeg"), "wb") as f:
                f.write(open(os.path.join(output_dir, filename), "rb").read())
            unique_hashes.add(hash_value)
            hashes[hash_value] = "köttbullar"

    print(f"Unique hashes: {len(unique_hashes)}")
    hashes = dict(sorted(hashes.items()))
    print(f"Hash map: {hashes}")
    print(file_hashes)
    
    classified_folder = "./assets/classified"
    # delete and recreate classified_folder
    if os.path.exists(classified_folder):
        for f in os.listdir(classified_folder):
            os.remove(os.path.join(classified_folder, f))
    os.makedirs(classified_folder, exist_ok=True)
    for hash_value, classification in classification_map.items():
        src = os.path.join(assets_dir, f"{hash_value}.jpeg")
        dst = os.path.join(classified_folder, f"{classification}_{hash_value}.jpeg")
        with open(dst, "wb") as out_f:
            out_f.write(open(src, "rb").read())

def decrypt_flag():
    bits = []
    for i in range(len(file_hashes)):
        filename = f"{i:04}.jpeg"
        hash_value = file_hashes[filename]
        classification = classification_map.get(hash_value, "unknown")
        bits.append("0" if classification == "köttbullar" else "1")
    bin_str = "".join(bits)
    chars = [chr(int(bin_str[i:i+8], 2)) for i in range(0, len(bin_str), 8)]
    flag = "".join(chars)
    print(f"Decrypted FLAG: {flag}")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    # encrypt_flag()
    classify_images()
    decrypt_flag()

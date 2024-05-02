#!/usr/bin/env python3
from typing import List, Dict
import json


def parse_mino(block, s: List[str]) -> Dict[str, str]:
    pass


def parse_block(s: List[str]) -> List[str]:
    block = {}
    block["block_type"] = s[0].split(" ")[0]

    paren_count = 0
    is_special = False
    for i, line in enumerate(s):
        if "{" in line:
            paren_count += 1
            if "Script" in line or "List" in line:
                is_special = True
        elif "}" in line:
            paren_count -= 1
            is_special = False
        else:
            if not is_special and line:
                parts = line.strip().split(" ")
                block[parts[0]] = " ".join(parts[1:])

        if paren_count == 0:
            return block, s[i + 2 :]

    return block, []


def tws_to_json(tws):
    tws_json = []
    if tws:
        tws_objects = [obj.strip()+"}" for obj in tws.split("}\n\n")]
        for tws_obj in tws_objects:
            tws_obj_json = {}
            tws_obj_json["type"] = tws_obj.split("{")[0].strip()

            for line in 

            tws_json.append(tws_obj_json)
    return tws_json



def parse_tws(filename):
    file = open(filename, "r").read()
    output = tws_to_json(file)

    return output



def main():
    output = parse_tws("CASCADE.TWS")
    if output:
        print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()

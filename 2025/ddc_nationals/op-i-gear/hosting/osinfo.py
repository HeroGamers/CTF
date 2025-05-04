#!/usr/bin/python3

import datetime
import platform
import random

DEBUG_FILE = "/tmp/osinfo.txt"

def write_debug_info():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_debug_info = {
        "OS": platform.system(),
        "Release": platform.release(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Random Number": random.randint(1, 100)
    }
    
    with open(DEBUG_FILE, "w") as file:
        file.write(f"Timestamp: {timestamp}\n")
        for key, value in random_debug_info.items():
            file.write(f"{key}: {value}\n")

if __name__ == "__main__":
    write_debug_info()

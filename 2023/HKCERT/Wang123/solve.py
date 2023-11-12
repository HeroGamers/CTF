import wtm_draw as draw
from wtm_model import WangTM

machine = WangTM(name="Flag Machine",
                 states=[char for char in "01456789ABCDEFGH"],
                 alphabet=[char for char in "hkcert23{flag}"],
                 blank_symbol="#",
                 transitions_string=" ".join([
                     "rRG fRH {RH aRH kR0 hR0 tRH fRH fRH aRH {R1 eR0 cR0 cRH gRH",  # 0
                     "aR5 }RH tRH 2RH lRH gRH tRH rRH 2RH aRH eRH fR1 fR4 gRH lRH",  # 1
                     "cR8 }RH aR5 tRH kRH 2RH }RH lRH 2RH kRH {RH aRH lRH fR1 tRH",  # 4
                     "kRF 2RH 2RH gRH kRE aRH gRH rRH lRH hRH }RH tRH fRH kRH 3RH",  # 5
                     "{RA eRH cRH gRH }RH tRH lRH aRH fRH 3RH fRH rRH gRH eRH {RH",  # 6
                     "2R9 kRH lRH {RH fRH fRH gRH hRH kRH 2RH lRH fRH hRH lRH hRH",  # 7
                     "3RE lRH eRH eRH kRH rRH eRH 3RH aRH gRH fRH tRH hRH gRH fRH",  # 8
                     "3R6 tRH 2RH fRH gRH eRH {RH hRH gRH {RH aRH lRH rRH }RH eRH",  # 9
                     "3RB fRH cRH {RH {RH {RH cRH gRH lRH hRH aRH 3RH aRH aRH fRH",  # A
                     "hR1 3RH hRH gRH {RH 3RH {RH gRH lRH aRH tRH aRH {RH gRH fRH",  # B
                     "}RH lRH rRH rRH kRH aRH cRH hRH cRH tRH }RH kRH eRH 3RH {RH",  # C
                     "rRC }RH rRH hRH {RH cRH 2RH tRH fRH aRH hRH 2RH rRH aRH cRH",  # D
                     "eRD hRH lRH 3RH tRH 2RH kRH eRH tRH lRH lRH lRH fRH rRH aRH",  # E
                     "kR4 eRH eRH cRH 3RH 2RH fRH 2RH {RH rRH cRH eRH aRH }RH tRH",  # F
                     "tR7 2RH fRH eRH gRH gRH fRH 2RH cRH aRH 3RH fRH aRH lRH tRH"  # G
                      # H
                 ]))

transitions = machine.transitions_string.split(" ")
for i in range(len(transitions)):
    transition = transitions[i]
    if len(transition) != 3:
        print(f"Transition {i} ({transition}) is not 3 characters long!")
        continue
    for char_i in range(len(transition)):
        char = transition[char_i]
        if char_i == 0:
            for alphabet_char in machine.alphabet:
                if char == alphabet_char:
                    break
            else:
                print(f"Transition {i} ({transition}) contains invalid alphabet character {char}!")
                continue
        elif char_i == 1:
            for direction_char in "LR":
                if char == direction_char:
                    break
            else:
                print(f"Transition {i} ({transition}) contains invalid direction character {char}!")
                continue
        elif char_i == 2:
            for state_char in machine.states:
                if char == state_char:
                    break
            else:
                print(f"Transition {i} ({transition}) contains invalid state character {char}!")
                continue

if machine:
    filename = draw.draw_tm(machine, input="real")
    print(filename)

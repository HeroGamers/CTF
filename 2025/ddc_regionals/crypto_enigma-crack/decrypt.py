#!/usr/bin/env python


# Install the engima machine python package!
# pip install py-enigma
from enigma.machine import EnigmaMachine


machine = EnigmaMachine.from_key_sheet(
    rotors='II III I', 
    reflector='B',      
    ring_settings='1 1 1',  
    plugboard_settings='AV BS CG DL FU HZ IN KM OW RX'  
)

# Message to be decrypted
plaintext = "" # Input here the flag
bracket_1 = "{"
bracket_2 = "}"

ciphertext = machine.process_text(plaintext)
print(f'Decrypted Flag: DDC{bracket_1}{ciphertext}_0{bracket_2}')








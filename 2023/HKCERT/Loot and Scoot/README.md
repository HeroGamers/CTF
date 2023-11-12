We can try to disassemble the game in IDA:

We see the function which we want to be called: on_flag_interact
This function reads flag.txt and gives it to us.

This function can be called from the onopen() function.
Inside this function we find some other forms of interactions, namely:
- on_default_interact
- on_default_enter
- on_flag_interact
- on_gate_1_interact
- on_gate_2_interact
- on_gate_3_interact
- on_gate_4_interact
- on_key_1_interact
- on_key_2_interact
- on_key_3_interact
- on_key_4_interact

We also find a walk function
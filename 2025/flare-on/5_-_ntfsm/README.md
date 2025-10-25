This appears to be a Non-deterministic Finite State Machine (NTFSM) challenge.
Can be solved by analyzing an objdump of the binary and extracting the state machine transitions.

❯ file ntfsm.exe
ntfsm.exe: MS PE32+ executable (console) x86-64

❯ binwalk ntfsm.exe

                       /home/hero/Documents/CTF/2025/flare-on/5_-_ntfsm/ntfsm.exe
--------------------------------------------------------------------------------------------------------
DECIMAL                            HEXADECIMAL                        DESCRIPTION
--------------------------------------------------------------------------------------------------------
0                                  0x0                                Windows PE binary, machine type:
                                                                      Intel x86-64
--------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 216.0 milliseconds


## Solution

The binary contains a massive state machine with ~90,000 states. Each state checks the current input character and transitions to the next state.

**Password:** `xXxqOv6oF5iDBZiw`

iqyMuXeZHn_psxYQ

### How it was solved:

1. Disassemble the binary using iced to get `ntfsm_disasm_2.txt`
2. Parse all handler blocks (identified by `jmp 0x140C685EE` - return to main loop)
3. Extract character comparisons and state transitions from each handler
4. Assume handlers appear in sequential state order (handler #N = state N)
5. Build a state transition graph
6. Use BFS from state 1 to find a 16-character path

See `solve_ntfsm_ordered.py` for the working solver.


## Strings:
https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ
cmd.exe
/c msg * Hello there, Hacker
open
Alert
The goal was never here to begin with.
This is our world now. The world of the electron and the switch; the beauty of the baud
That was a complete waste of time.
Nothing to see here, move along.
You are likely somewhat close.
My crime is that of curiosity. I am a hacker, and this is my manifesto
No seriously, i hope it can not be bruteforced
The cake is a lie.
We appreciate your efforts, but due to a strategic realignment, the project's scope has been expanded.
These are not the droids you're looking for.
The princess is in another castle.
A strange game. The only winning move is not to play
Sorry, this was just the decoy.
This was a side quest. The main story is elsewhere.
Good effort!
Sandboxes hate this one weird trick
I hope you are not trying to bruteforce this
You've been redirected. Please try another server.
Something went wrong!
invalid argument
state
input
position
transitions
correct!
wrong!
usage: ./ntfsm <password>
to reset the binary in case of weird behavior: ./ntfsm -r
input 16 characters
Your reward: %s


16 characters password needed
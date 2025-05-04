.intel_syntax noprefix
.global _start
.section .text

macros:
    .macro syscall_read buf count
        mov edx, \count
        lea rsi, \buf
        xor edi, edi
        xor eax, eax
        syscall
    .endm

    .macro syscall_write buf count
        mov edx, \count
        lea rsi, \buf
        mov edi, 0x1
        mov eax, 0x1
        syscall
    .endm

    .macro syscall_exit
        xor edi, edi
        xor eax, eax
        mov eax, 0x3c
        syscall
    .endm

_start:

    syscall_write [hello], (offset hello_len)
    call get_input
    call emit
    call sneaky
    call swappy
    call exit

get_input:

    syscall_read [buf], 0x10
    bt ax, 0
    jc exit
    mov r15b, al
    ret

emit:

    mov eax, 0x90c39066
    lea edi, [t]
    1: stosd
    inc ah
    cmp ah, 0x99
    jne 1b
    ret

swappy:

    movzxb r8, [buf + r10]
    movzxb r9, [buf + r10 + 1]
    sub r8b, 0x30
    cmp r8b, 0x9
    ja exit
    mov al, r9b
    lea r11, [t + r8 * 4]
    call r11
    add r10b, 2
    sub r15b, 2
    jnz swappy
    ret

win: syscall_write [flag], (offset flag_len)
exit: syscall_write [bye], (offset bye_len); syscall_exit

.section sneaky, "awx"

        rdrand bx
        jnc sneaky
        and bl, 0xf8
        mov rax, -0x100
        xord $+18, 0xeb03d334
        andn rax, rsp, rax
        imul rsp
        fcmovnu st, st(3)
        imul ecx, esp, 0xf
        movq [rax - 0x1000], offset win
        1: xchg r8, rsp
        xor eax, eax
        addb $-1, 9
        jnc 1b
        ret

    .lcomm buf 0x100
    .lcomm t (0x4 * 0x9)

.section .rodata

    flag: .string "DDC{fake_flag_for_testing}\n" ;.equ flag_len, ($ - flag) - 0x1
    hello: .string "hello~\n"; .equ hello_len, ($ - hello) - 0x1
    bye: .string "bye~\n"; .equ bye_len, ($ - bye) - 0x1

// as -64 -o swappy.o swappy.s && ld --oformat=elf64-x86-64 -EL --no-warn-rwx-segments -o swappy swappy.o

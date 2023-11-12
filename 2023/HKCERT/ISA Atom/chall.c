#include <stdio.h>
#include <stdlib.h>

int func2(int arg1, int arg2) {
    int R2, R4, R3, R1, R5;

    R2 = arg1;  // MOV R2, [FP+12];
    R4 = arg2;  // MOV R4, [FP+8];

    R3 = R4 & R2;  // MOV R3, R4;
                   // AND R3, R2;
    R1 = R3 << 1;  // MOV R1, R3;
                   // SHL R1, 1;
    R5 = R4 ^ R2;  // MOV R5, R4;
                   // XOR R5, R2;
    R3 = R5 + R1;  // MOV R3, R5;
                   // ADD R3, R1;
    R1 = R3;       // MOV R1, R3;

    return R1;
}

int func1(int arg) {
    int R5 = arg;  // MOV R5, [FP+8];

    if (R5 <= 2) {  // LTE R5, 2;
        return 1;   // MOV R3, R1;
                    // MOV R1, 1;
    } else {
        int R6 = R5 - 1;  // MOV R6, R5;
                          // SUB R6, 1;
        int R4 = R6;      // MOV R4, R6;

                          // PUSH R4;
                          // MOV [FP+8], R5;
                          // MOV [FP-8], R4;

        int R1 = func1(R4);  // CALL 0x4000d9;
        R1 *= 2;      // MOV R4, 2;
                      // MUL R4, R1;
                      // MOV R1, [FP-8];
                      // MOV R1, R4;
                      // MOV R5, [FP+8];

        R4 = R5 - 2;  // MOV R4, R5;
                      // SUB R4, 2;

        int R2 = R4;              // MOV R2, R4;
                        //PUSH R2;
                        //MOV [FP+8], R5;
                        //MOV [FP-8], R1;
                        //MOV [FP-12], R2;
        R2 = func1(R4);  // CALL 0x4000d9;
                             // MOV R2, [FP-12];
                             //MOV R2, R1;
                             //PUSH R2;
                             //MOV R1, [FP-8];
                             //PUSH R1;
        //MOV [FP-8], R1;
        //MOV [FP-12], R2;
        R1 = func2(R1, R2);  //CALL 0x400014;		call func2
        //MOV R2, R1;
        //MOV R1, R2;

        return R1;
    }
}

int loop(int R5, unsigned int *stack) {
    unsigned int R2, R4, R1;

    while (R5 < 100) {
        R1 = func1(R5);  // MOV [FP-104], R5;
        // CALL 0x4000d9;
        R2 = R1 & 255;       // MOV R2, R1;
        // AND R2, 255;
        R4 = R2;             // MOV R4, R2;

        R1 = stack - 100;  // MOV R1, FP;
        // SUB R1, 100;
        R2 = R1 + R5;     // MOV R2, R1;
        // ADD R2, R5;
        stack[R2] ^= R4;

        R1 = *stack - 100;
        R2 = R1 + stack[26];
        stack[R2] ^= (R1 + stack[26]);
        stack[R1 + stack[26]] ^= R2;
        stack[R2] ^= (R1 + stack[26]);

        putchar(R1);  // MOV R2, 1;
                         // MOV R8, 1;
                         // SYSCALL;
        R5 += 1;
    }

    return 0;
}

int main() {
    unsigned int stack[104];
    int R5;

    stack[0] = 0x8341013f;
    stack[1] = 0x83391117;
    stack[2] = 0xe35141cf;
    stack[3] = 0xa3899167;
    stack[4] = 0xc3e101df;
    stack[5] = 0x43599137;
    stack[6] = 0x23f1416f;
    stack[7] = 0x63a91187;
    stack[8] = 0x381017f;
    stack[9] = 0x3791157;
    stack[10] = 0x6391410f;
    stack[11] = 0x23c991a7;
    stack[12] = 0x3e1e602a;
    stack[13] = 0xaac6fc18;
    stack[14] = 0x940434cc;
    stack[15] = 0xbcdd4ea9;
    stack[16] = 0xb39e6f8f;
    stack[17] = 0xea8e25ed;
    stack[18] = 0xd2bc703b;
    stack[19] = 0xd339ce89;
    stack[20] = 0xa23e362a;
    stack[21] = 0x73bba5e8;
    stack[22] = 0x54412994;
    stack[23] = 0x501b6575;
    stack[24] = 0x66626a69;

    R5 = 0;             // MOV R5, 0;

    loop(R5, stack);

    exit(0);  // R2 = R1;
              // MOV R1, 0;
              // MOV R8, 2;
              // SYSCALL;
}
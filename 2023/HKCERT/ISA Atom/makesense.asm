JMP 0x400321;      main
func2:	PUSH FP;	0x400014
		MOV FP, SP;
		SUB SP, 4;
		MOV R2, [FP+12];
		MOV R4, [FP+8];
		MOV R3, R4;
		AND R3, R2;
		MOV R1, R3;
		SHL R1, 1;
		MOV R5, R4;
		XOR R5, R2;
		MOV R3, R5;
		ADD R3, R1;
		MOV R1, R3;
		MOV SP, FP;
		POP FP;
		RET;

func1: 	PUSH FP;     	0x4000d9
		MOV FP, SP;
		SUB SP, 12;
		MOV R5, [FP+8];
		LTE R5, 2;
		JNZ +9;
		JMP +48;       goto MOV R6, R5;
		MOV R3, R1;
		MOV R1, 1;
		MOV SP, FP;
		POP FP;
		RET;

MOV R6, R5;
SUB R6, 1;
MOV R4, R6;
PUSH R4;
MOV [FP+8], R5;
MOV [FP-8], R4;
CALL 0x4000d9;		call func1
ADD SP, 4;
MOV R4, 2;
MUL R4, R1;
MOV R1, [FP-8];
MOV R1, R4;
MOV R5, [FP+8];
MOV R4, R5;
SUB R4, 2;
MOV R2, R4;
PUSH R2;
MOV [FP+8], R5;
MOV [FP-8], R1;
MOV [FP-12], R2;
CALL 0x4000d9;   	call func1
ADD SP, 4;
MOV R2, [FP-12];
MOV R2, R1;
PUSH R2;
MOV R1, [FP-8];
PUSH R1;
MOV [FP-8], R1;
MOV [FP-12], R2;
CALL 0x400014;		call func2
ADD SP, 8;
MOV R2, R1;
MOV R1, R2;
MOV SP, FP;
POP FP;
RET;    what is this RET doing here

main: 	SUB SP, 104;   0x400321
		MOV R2, SP;
		MOV SP, FP;
		SUB SP, 0;
		PUSH 0x8341013f;
		PUSH 0x83391117;
		PUSH 0xe35141cf;
		PUSH 0xa3899167;
		PUSH 0xc3e101df;
		PUSH 0x43599137;
		PUSH 0x23f1416f;
		PUSH 0x63a91187;
		PUSH 0x381017f;
		PUSH 0x3791157;
		PUSH 0x6391410f;
		PUSH 0x23c991a7;
		PUSH 0x3e1e602a;
		PUSH 0xaac6fc18;
		PUSH 0x940434cc;
		PUSH 0xbcdd4ea9;
		PUSH 0xb39e6f8f;
		PUSH 0xea8e25ed;
		PUSH 0xd2bc703b;
		PUSH 0xd339ce89;
		PUSH 0xa23e362a;
		PUSH 0x73bba5e8;
		PUSH 0x54412994;
		PUSH 0x501b6575;
		PUSH 0x66626a69;
		MOV SP, R2;
		MOV R5, 0;
		PUSH R5;			called again from JNZ -362
		MOV [FP-104], R5;
		CALL 0x4000d9;		call func1
		ADD SP, 4;
		MOV R2, R1;
		AND R2, 255;
		MOV R4, R2;
		MOV R1, FP;
		SUB R1, 100;
		MOV R2, R1;
		MOV R5, [FP-104];
		ADD R2, R5;
		XOR [R2], R4;
		MOV R1, FP;
		SUB R1, 100;
		MOV R2, R1;
		ADD R2, R5;
		XOR R2, R1;
		XOR R1, R2;
		XOR R2, R1;
		MOV R6, R2;
		MOV R2, 1;
		MOV R8, 1;
		SYSCALL;		print out char
		MOV R1, R2;
		ADD R5, 1;
		LT R5, 100;
		MOV [FP-104], R5;
		JNZ -362;		goto PUSH R5
		MOV R2, R1;
		MOV R1, 0;
		MOV R8, 2;
		SYSCALL;		exit
		ADD SP, 104;
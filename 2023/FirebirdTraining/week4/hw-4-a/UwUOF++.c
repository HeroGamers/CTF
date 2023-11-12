#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int passcode;

void UwU_flag(int arg1, int arg2, int arg3, int arg4,
			  int arg5, int arg6, int arg7, int arg8,
			  int arg9, int arg10, int arg11, int arg12) {
	char flag[42];
	char input[6];
	puts("What the hack!! How you did get here!! (ꐦ°᷄д°᷅) ");
	puts("But this time, you will need the passcode in order to get the flag (´∩ω∩｀)");
	FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
            printf("flag.txt file is missing (′゜ω。‵)\n");
            exit(1);
    }
    printf("* Please enter the passcode: ");
	fgets(input, 6, stdin);
	if (passcode == atoi(input)) {
		if (arg8 != 0xdeadbeef) {
			printf("Your 8th argument is not 0xdeadbeef •_ゝ•");
			exit(1);
		}
		if (arg11 != 0xbeefdead) {
			printf("Your 11th argument is not 0xbeefdead •_ゝ•");
			exit(1);
		}
        fgets(flag, 42, f);
		puts("You beat me... Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾");
		puts(flag);
    }
    exit(1);
}

void know_more_about_UwU() {
	char addr[20];
	printf("\nGive UwU an address and UwU will tell you what is in that address!\n");
	printf("* Please enter an address e.g. 0x7fffdeadbeef: ");
	fgets(addr, 20, stdin);
	printf("That address contains %p\n\n", *(unsigned long long *)(void *)strtol(addr, NULL, 0));
}

void UwU_main() {
	char choice[2];
	char UwU[8] = "UwU";
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");

	puts("UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ\n");
	printf("Therefore, UwU is good enough to let you know you are in %p now（´◔ ₃ ◔`)\n", UwU_main);
	printf("and UwU is in %p\n\n", UwU);

	puts("Btw, do you want to know more about the world of UwU?");
	printf("* Please enter a choice (1:Yes, 2:Yes): ");
	fgets(choice, 2, stdin);
	getchar();

	if ((atoi(choice) == 1) || (atoi(choice) == 2)) {
		know_more_about_UwU();
	} else {
		puts("\nYou don't want to know more about UwU? (′゜ω。‵)\n");
	}

	puts("Then, can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	gets(buffer);
    
	char* ptr = strstr(buffer, "UwU");
    if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL) {
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		if (strcmp(UwU, "UwU") != 0) {
			exit(1);
		}
    } else {
		puts("Your input is not UwU enough!! _(┐ ◟;ﾟдﾟ)ノ");
		exit(1);
	}
}


int main() {
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);

	srand(time(NULL));
    passcode = rand() % 100000;

	UwU_main();

	puts("See you next time!!（๑ • ‿ • ๑ ）\n");
	return 0;
}
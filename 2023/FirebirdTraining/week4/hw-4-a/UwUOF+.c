#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void UwU_flag() {
	char flag[48];
	puts("What the hack!! How you did get here!! (ꐦ°᷄д°᷅) ");
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL) {
		printf("flag.txt file is missing (′゜ω。‵)\n");
		exit(0);
	}
	fgets(flag, 48, f);
	puts("Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾");
	puts(flag);
}

void UwU_main() {
    char UwU[8] = "nothing";
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");
	puts("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	gets(buffer);
	// I have added some requirements you need to pass ( ^ω^)
    char* ptr = strstr(buffer, "UwU");
    if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL) {
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		// Now, badbad people can't get into UwU_flag that easily ( ^ω^)
		if (strcmp(UwU, "nothing") != 0) {
			// UwU_flag();
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

	UwU_main();

	puts("See you next time!!（๑ • ‿ • ๑ ）\n");
	return 0;
}
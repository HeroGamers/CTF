#include <stdio.h>
#include <stdlib.h>

void UwU_main() {
    char UwU[0x10];
    unsigned long long *ptr = UwU+0x18;
    puts("");
    puts("");
    printf("||        ||   %p   ||        ||\n", &UwU);
    printf("||        || %p ||        ||\n", *ptr);
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||     ||      ||     ||        ||\n");
    printf("||        ||     ||  ||  ||     ||        ||\n");
    printf("||        ||     ||  ||  ||     ||        ||\n");
    printf("  ========         ==  ==         ========  \n");
    puts("");
    puts("");

    puts("The world of UwU need your help! Can you give me a shellcode for the king of UwU to run?");
    fgets(UwU, 0x30, stdin);
    puts("Thanks for your help!");
}

int main() {
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
	UwU_main();
	return 0;
}
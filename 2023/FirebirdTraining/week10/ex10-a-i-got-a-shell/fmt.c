#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char random2[4];
int random3 = 0;

void readline(char *buf, int len) {
    int l = read(0, buf, len - 1);
    if (buf[l - 1] == '\n') buf[l - 1] = '\0';
    buf[l] = '\0';
}

void printflag(const char *name) {
    char flag[100];

    FILE *flagfile = fopen(name, "r");

    if (flagfile == NULL) {
        perror("failed to open flag file");
        exit(1);
    } else {
        fread(flag, sizeof(flag), 1, flagfile);
        puts(flag);
    }

    fclose(flagfile);
}

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
}

int main() {
    char random1[8];

    char buf[0x100];

    init();
    memset(random1, '\0', 8);

    FILE *random = fopen("/dev/urandom", "r");

    if (random == NULL) {
        perror("failed to open urandom");
        exit(1);
    } else {
        fread(random1, 4, 1, random);
        fread(random2, 4, 1, random);
    }

    fclose(random);

    printf("Welcome to the format string playground!\n");
    printf("Give me your first input:");
    readline(buf, 0x100);
    printf("Your input:");
    printf(buf);

    printf("\nGive me the random number you got:");
    readline(buf, 0x100);
    printf("Your input: %s\n", buf);

    if (strcmp(random1, buf) == 0) {
        printflag("flag1.txt");
    } else if (strcmp(random2, buf) == 0) {
        printflag("flag2.txt");
    } else if (random3 == 0x1234321) {
        printflag("flag3.txt");
    }
    return 0;
}

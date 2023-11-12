#include <stdio.h>

int main(void) {
    int i;
    int count;

    unsigned char data[] = {0x55, 0x38, 0x5b, 0x31, 0xb1, 0x8e, 0xb3, 0xed, 0x8b,
                            0x1d, 0xaf, 0x50, 0x6e, 0xb6, 0x25, 0x6a, 0xf6,
                            0x79, 0xec, 0x4e, 0x6f, 0x1b, 0x2a, 0x6e, 0xe4,
                            0x74, 0x08, 0xbf, 0x8d};

    unsigned char fibonacci[] = {0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

    unsigned char input[29];

    printf("Data: ");
    for (i = 0; i < 29; i = i + 1) {
        printf("%d ", data[i]);
    }
    puts("");

    for (i = 2; i < 29; i = i + 1) {
        fibonacci[i] = fibonacci[i - 1] + fibonacci[i - 2];
    }

    printf("Fibonacci: ");
    for (i = 0; i < 29; i = i + 1) {
        printf("%d ", fibonacci[i]);
    }
    puts("");

    printf("Input: \n");
    for (i = 0; i < 29; i = i + 1) {
        scanf("%c", input + i);
        printf("%d ", input[i]);
        input[i] = input[i] + fibonacci[i];
    }
    puts("");

    printf("Modified input: ");
    for (i = 0; i < 29; i = i + 1) {
        printf("%d ", input[i]);
    }
    puts("");

    count = 0;
    for (i = 0; i < 29; i = i + 1) {
        input[i] = input[i] ^ input[(i + 28) % 29];
        if (input[i] == data[i]) {
            count = count + 1;
        }
    }

    printf("Final input: ");
    for (i = 0; i < 29; i = i + 1) {
        printf("%d ", input[i]);
    }
    puts("");

    printf("Count: %d\n", count);

    if (count == 29) {
        puts(":D");
    }
    else {
        puts(":(");
    }

    return 0;
}
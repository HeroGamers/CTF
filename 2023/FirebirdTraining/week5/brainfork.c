#include <stdio.h>

char *main_input = "772777779061980000008777777777778000000827777790619827900061977800000000877777777800000000877279"
                   "000619800000082777906197777877778000008972777779061980000002790061987777777778777777877778000000"
                   "000000087777777777780000000000000877777778972777906198972777779061908000008000000000000827779000"
                   "006198002790006198008972777906197778972777779061987772790061978727900000061908002790061908027777"
                   "790061978000000089727779061987727779061977787777777777777778277790619800877800000000890000000000"
                   "8";

char *special_chars = "^&_=\\,.#$!+-@*>[</}{:])(";
char *cjilegbdfahmkn = "cjilegbdfahmkn";
unsigned int output;



int func_1(char *input) {
    int special_char;
    int v3;
    unsigned int v5;
    unsigned int i;
    int string_1[4096];
    int number_1 = 0;
    int word_122C0[512];
    int word_E2C2[8192];

    for (i = 0; *input && i <= 0xFFFu; ++i) {
        special_char = special_chars[cjilegbdfahmkn[(char) *input - 48] - 87];
        if (special_char == 125)                  // }
        {
            *((char *) &string_1 + 2 * i) = 7;
            if (number_1 == 512)
                return 1;
            v3 = number_1++;
            word_122C0[v3] = i;
        } else {
            if (special_char > 125)                 // > }
                goto LABEL_21;
            if (special_char > 64)                  // > @
            {
                if (special_char != 123)              // != {
                {
                    LABEL_21:
                    --i;
                    goto LOOP_ITERATE;
                }
                if (!number_1)
                    return 1;
                v5 = word_122C0[--number_1];
                *((char *) &string_1 + 2 * i) = 8;
                word_E2C2[2 * i] = v5;
                word_E2C2[2 * v5] = i;
            } else {
                if (special_char < 42)                // < *
                    goto LABEL_21;
                switch (special_chars[cjilegbdfahmkn[(char) *input - 48] - 87]) {
                    case '*':
                        *((char *) &string_1 + 2 * i) = 4;
                        break;
                    case '+':
                        *((char *) &string_1 + 2 * i) = 1;
                        break;
                    case '-':
                        *((char *) &string_1 + 2 * i) = 2;
                        break;
                    case '<':
                        *((char *) &string_1 + 2 * i) = 6;
                        break;
                    case '>':
                        *((char *) &string_1 + 2 * i) = 5;
                        break;
                    case '@':
                        *((char *) &string_1 + 2 * i) = 3;
                        break;
                    default:
                        goto LABEL_21;
                }
            }
        }
        LOOP_ITERATE:
        ++input;
    }
    if (number_1 || i == 4096)
        return 1;
    *((char *) &string_1 + 2 * i) = 0;
    return 0;
}


int func_1_old(char *input) {
    int special_char;
    int v3;
    unsigned int v5;
    unsigned int i;
    int string_1[4096];
    int number_1 = 0;
    int word_122C0[512];
    int word_E2C2[8192];

    for (i = 0; *input && i <= 0xFFFu; ++i) {
        special_char = special_chars[cjilegbdfahmkn[(char) *input - 48] - 87];
        if (special_char == 125)                  // }
        {
            *((char *) &string_1 + 2 * i) = 7;
            if (number_1 == 512)
                return 1LL;
            v3 = number_1++;
            word_122C0[v3] = i;
        } else {
            if (special_char > 125)                 // > }
                goto LABEL_21;
            if (special_char > 64)                  // > @
            {
                if (special_char != 123)              // != {
                {
                    LABEL_21:
                    --i;
                    goto LOOP_ITERATE;
                }
                if (!number_1)
                    return 1LL;
                v5 = word_122C0[--number_1];
                *((char *) &string_1 + 2 * i) = 8;
                word_E2C2[2 * i] = v5;
                word_E2C2[2 * v5] = i;
            } else {
                if (special_char < 42)                // < *
                    goto LABEL_21;
                switch (special_chars[cjilegbdfahmkn[(char) *input - 48] - 87]) {
                    case '*':
                        *((char *) &string_1 + 2 * i) = 4;
                        break;
                    case '+':
                        *((char *) &string_1 + 2 * i) = 1;
                        break;
                    case '-':
                        *((char *) &string_1 + 2 * i) = 2;
                        break;
                    case '<':
                        *((char *) &string_1 + 2 * i) = 6;
                        break;
                    case '>':
                        *((char *) &string_1 + 2 * i) = 5;
                        break;
                    case '@':
                        *((char *) &string_1 + 2 * i) = 3;
                        break;
                    default:
                        goto LABEL_21;
                }
            }
        }
        LOOP_ITERATE:
        ++input;
    }
    if (number_1 || i == 4096)
        return 1LL;
    *((char *) &string_1 + 2 * i) = 0;
    return 0LL;
}

int func_2(char *input) {
    int v1[65540];
    int i;
    int v3;

    v3 = 0;
    for (i = 0xFFFF; --i; v1[i] = 0);
    if (output == 42)
        output = -252645158;
    return 1LL;
}

int main(int a1, char **a2, char **a3) {
    output = func_1(main_input);
    if (output == 1)
        output = func_2(main_input);
    else
        fwrite("Error!\n", 1uLL, 7uLL, stderr);
    return (unsigned int) output;
}

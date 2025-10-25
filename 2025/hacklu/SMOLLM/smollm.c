#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>

#define TOKEN_SIZE 8

char tokens[256][TOKEN_SIZE] = { 0 };
int n_tokens = 0;

const char *init_tokens[] = {
    "a",
    "about",
    "all",
    "also",
    "and",
    "as",
    "at",
    "be",
    "because",
    "but",
    "by",
    "can",
    "come",
    "could",
    "computer",
    "ctf",
    "day",
    "do",
    "even",
    "find",
    "first",
    "flux",
    "for",
    "from",
    "get",
    "give",
    "go",
    "hacklu",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "I",
    "if",
    "in",
    "into",
    "it",
    "its",
    "just",
    "know",
    "like",
    "look",
    "make",
    "man",
    "many",
    "me",
    "more",
    "mvm",
    "my",
    "new",
    "no",
    "not",
    "now",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "our",
    "out",
    "people",
    "plfanzen",
    "say",
    "see",
    "she",
    "so",
    "some",
    "take",
    "tell",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "thing",
    "think",
    "this",
    "those",
    "time",
    "to",
    "two",
    "up",
    "use",
    "very",
    "want",
    "way",
    "we",
    "well",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "year",
    "you",
    "your",
};

void add_token(const char* token, int len) {
    if (n_tokens == 256) {
        printf("Max number of tokens reached!\n");
        return;
    }
    memcpy(tokens[n_tokens], token, len);
    memset(tokens[n_tokens++] + len, ' ', TOKEN_SIZE - len);
}

void run_prompt() {
    int n;
    static unsigned int combinator = 0;
    char in_buf[256], out_buf[256];
    bzero(in_buf, sizeof(in_buf));
    bzero(out_buf, sizeof(in_buf));

    printf("How can I help you?\n>");
    n = read(STDIN_FILENO, in_buf, sizeof(in_buf));
    if (n <= 0) {
        printf("Read error\n");
        exit(-1);
    }
    for (int i = 0; i < n; i++) {
        memcpy(&out_buf[i*TOKEN_SIZE], tokens[(in_buf[i] + combinator++) % n_tokens], TOKEN_SIZE);
    }

    printf(out_buf);
    printf("\n");
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    for (int i = 0; i < sizeof(init_tokens) / sizeof(*init_tokens); i++) {
        add_token(init_tokens[i], strlen(init_tokens[i]));
    }
}

int main(int argc, char *argv[]) {
    int n;
    char buf[9];
    init();

    printf("Hello, and welcome to smøllm. Your friendly AI assistant.\nYou can add you own custom tokens or run a prompt.\n");

    while (1) {
        printf("Do you want to\n1) Add a custom token\n2) Run a prompt\n>");
        if (read(STDIN_FILENO, buf, sizeof(buf)) <= 0) {
            printf("Read error\n");
            exit(-1);
        }
        if (buf[0] == '1') {
            memset(buf, 0, sizeof(buf));
            printf("token?>");
            n = read(STDIN_FILENO, buf, TOKEN_SIZE);
            if (n <= 0) {
                printf("Read error\n");
                exit(-1);
            }
            add_token(buf, n);
        } else if (buf[0] == '2') {
            run_prompt();
        } else {
            printf("Invalid choice\n");
        }
    }
}

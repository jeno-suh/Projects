#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void check(int return_val, char *error_msg) {
    if (return_val < 0) {
        printf("Error: %s\n", error_msg);
        exit(EXIT_FAILURE);
    }
}

void check_thread(int return_val, char *error_msg) {
    if (return_val != 0) {
        printf("Error: %s\n", error_msg);
        exit(EXIT_FAILURE);
    }
}

bool alnum(char *string) {
    int n = strlen(string);
    for(int i = 0; i < n; i++) {
        if (!isalnum(string[i])) {
            return false;
        }
    }
    return true;
}

bool starts_with(char *string, char *substring) {
    return strncmp(string, substring, strlen(substring)) == 0;
}
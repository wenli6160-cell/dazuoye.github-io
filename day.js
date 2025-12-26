#include <stdio.h>
#include <string.h>

int main() {
    char str[81];
    int seen[26] = {0};
    int has_upper = 0;

    fgets(str, 81, stdin);

    for (int i = 0; i < strlen(str); i++) {
        char c = str[i];
        if (c >= 'A' && c <= 'Z') {
            int index = c - 'A';
            if (!seen[index]) {
                putchar(c);
                seen[index] = 1;
                has_upper = 1;
            }
        }
    }

    if (!has_upper) {
        printf("Not Found");
    }
    printf("\n");

    return 0;
}
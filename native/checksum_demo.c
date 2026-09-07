/*
 * LABYRINTH checksum demo helper.
 * Educational optional component.
 */
#include <stdio.h>

int main(int argc, char** argv) {
    unsigned long hash = 5381;
    int c;
    FILE* f;

    if (argc < 2) {
        printf("usage: checksum_demo <file>\\n");
        return 1;
    }

    f = fopen(argv[1], "rb");
    if (!f) {
        printf("could not open file\\n");
        return 1;
    }

    while ((c = fgetc(f)) != EOF) {
        hash = ((hash << 5) + hash) + (unsigned char)c;
    }

    fclose(f);
    printf("%lu\\n", hash);
    return 0;
}

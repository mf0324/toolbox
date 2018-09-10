#include <stdio.h>
#include <string.h>

int main() {
    char name[20] = "chris ";
    char kbd[20] = "ordinary";
    strcat(name, kbd);
    printf("[%s]\n", name);

    return 0;
}

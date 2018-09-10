#include <stdio.h>

int main() {
    char* txt_pth = "test.txt";
    FILE* fp = fopen(txt_pth, "r");
    if (fp==NULL) {
        printf("opening %s fails!\n", txt_pth);
        return -1;
    }
    char im_pth[100];
    while(1) {
        int ret = fscanf(fp, "%s", im_pth);
        if (ret==-1) {
            break;
        }
        printf("%s, ret=%d\n", im_pth, ret);
    }
    fclose(fp);

    return 0;
}

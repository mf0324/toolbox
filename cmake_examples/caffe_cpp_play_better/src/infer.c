#include <stdio.h>
#include <string.h>

int hoho(int argc, char** argv) {
    if (argc<2) {
        printf("usage: ./a.out test.txt\n");
        return -1;
    }
    char* im_lst = argv[1];
    FILE* fp = fopen(im_lst, "r");
    char im_name[20];
    char im_dir[100] = "/home/zz/data/BDCI_preliminary/JPEGImages/";
    char im_pth[256];
    while(1) {
        int ret = fscanf(fp, "%s", im_name);
        if (ret==-1) {
            break;
        }
        memset(im_pth, 0, sizeof(im_pth));
        strcpy(im_pth, im_dir);
        strcat(im_pth, im_name);
        printf("[%s]\n", im_pth);
    }
    fclose(fp);

    return 0;
}

void test(){
    char str[20] = "google"; // len = 6
    size_t len = strlen(str);
    printf("%zd\n", len);
}

int main(int argc, char** argv) {
    hoho(argc, argv);
    return 0;
}

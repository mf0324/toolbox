#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
 * C语言中，逐行读取文本文件，有两种函数可用：
 *  - fgets(buf, sizeof(buf), fp) != NULL
 *  - getline(buf, &sz, fp) > 0
 * 它们都以换行符或达到最大长度结束。具体例子如下。
 */


/*
 * 方法1：用fgets()读取一行，
 * 读取到的line以`\n`截断，或者达到设定的最大长度时截断。
 *
 * 缺点：
 *   需要提前预估每行的最长字符长度；
 */
int read_txt_line_by_line_method1(char* txt_pth) {
    FILE* fp = fopen(txt_pth, "r");
    size_t max_len = 1024;
    if (fp==NULL) {
        printf("!cannot open file %s\n", txt_pth);
        return -1;
    }
    char line[max_len];
    while(fgets(line, sizeof(line), fp)) {
        printf("%s", line);
    }
    fclose(fp);
    return 0;
}


/*
 * 方法2：使用getline
 * 现代一点的C语言编译器是支持getline的
 *
 * 缺点：
 *   依然需要预先估计每一行的最大长度
 *   要记得释放buf
 */
int read_txt_line_by_line_method2(char* txt_pth) {
    size_t max_len = 1024;
    char* buf = NULL;
    FILE* fp = fopen(txt_pth, "r");
    while(getline(&buf, &max_len, fp)>0) {
        printf("%s", buf);
    }
    free(buf);
    buf=NULL;
    fclose(fp);
    return 0;
}



int main() {
    char* txt_pth = "test.txt";
    read_txt_line_by_line_method1(txt_pth);
    printf("=================\n");
    read_txt_line_by_line_method2(txt_pth);

    return 0;
}

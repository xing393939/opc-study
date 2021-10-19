#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>

#define PROFILE_FUNC(func, ...) \
{ long start = clock(); func(__VA_ARGS__); printf("=== %.3fs for " #func " ===\n", (double) (clock() - start) / 1000); }

typedef struct Stu {
    char name[50];
    int id;
} Stu;

void my_fwrite(char *path) {
    FILE *fp = NULL;

    //"w+"，读写方式打开，如果文件不存在，则创建; 如果文件存在，清空内容，再写
    fp = fopen(path, "w+");
    if (fp == NULL) {
        perror("my_fwrite fopen");
        return;
    }

    Stu s[3000];
    char buf[50] = {0};
    for (int i = 0; i < 3000; i++) {
        sprintf(buf, "stu%d%d%d", i, i, i);
        strcpy(s[i].name, buf);
        s[i].id = i + 1;
    }

    unsigned long long ret = fwrite(s, sizeof(Stu), 3000, fp);
    printf("ret_write = %llu\n", ret);

    fclose(fp);
}

void my_fread(char *path) {
    FILE *fp = NULL;
    fp = fopen(path, "r+");
    if (fp == NULL) {
        perror("my_fread fopen");
        return;
    }

    Stu s[3000];
    unsigned long long ret = fread(s, sizeof(Stu), 3000, fp);
    printf("ret_read = %llu\n", ret);

    for (int i = 0; i < 3000; i++) {
        printf("s[%d] = %s, %d ", i, s[i].name, s[i].id);
    }
    printf("\n");

    fclose(fp);
}

void mmap_read(char *path) {
    int ln = sizeof(Stu) * 3000;
    int fd;
    Stu *s;
    fd = open(path, O_RDWR);
    s = mmap(NULL, ln, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (s == MAP_FAILED)
        return;
    for (int i = 0; i < 3000; i++) {
        printf("s[%d] = %s, %d ", i, s[i].name, s[i].id);
    }
    printf("\n");

    // 内存修改第0条记录
    strcpy(s[0].name, "aaa000");

    munmap(s, ln);
    close(fd);
}

void func1() {
    sleep(1);
}

void func2(int a, int b) {
    sleep(b);
}

int main() {
    char *f = "./004.txt";
    PROFILE_FUNC(my_fwrite, f);
    PROFILE_FUNC(mmap_read, f);
    PROFILE_FUNC(my_fread, f);

    PROFILE_FUNC(func1);
    PROFILE_FUNC(func2, 1, 3);
}
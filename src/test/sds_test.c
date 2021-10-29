#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sds.h"

int main(void) {

    sds empty = sdsempty();
    sdscat(empty,"hahah");
    size_t i = sdsavail(empty);
    printf("avail length:%d", i);
    return 0;

}

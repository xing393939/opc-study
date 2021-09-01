#include <stddef.h>

/* 额外增加start */
void *zmalloc(size_t size) {
    return malloc(size);
}
void *zcalloc(size_t size) {
    return malloc(size);
}
void *zrealloc(void *ptr, size_t size) {
    return realloc(ptr, size);
}
void zfree(void *ptr) {
    free(ptr);
}
/* 额外增加end */
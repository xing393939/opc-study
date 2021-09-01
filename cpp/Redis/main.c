#include <stdio.h>
#include "dict.h"
#include "intset.h"

unsigned int hashFunction(const void *str) {
    return (unsigned int) str;
}

int main(int argc, char *argv[]) {
    dictType hash_type;
    hash_type.hashFunction = hashFunction;
    hash_type.keyDup = 0;
    hash_type.valDup = 0;
    hash_type.keyCompare = 0;
    char *arr[] = {"key1", "key2", "key3", "val1", "val2", "val3"};

    // 字典：create
    dict *my_dict = dictCreate(&hash_type, 0);

    // 字典：set key val
    dictReplace(my_dict, arr[0], arr[3]);
    dictReplace(my_dict, arr[1], arr[4]);

    // 字典：get key
    printf("key1: %s\n", dictFetchValue(my_dict, "key1"));
    printf("key2: %s\n", dictFetchValue(my_dict, "key2"));

    // 整型集合
    intset * my_ints = intsetNew();
    intsetAdd(my_ints, 97, 0);
    intsetAdd(my_ints, 98, 0);
    printf("get: %d\n", intsetFind(my_ints, 97));
    printf("get: %d\n", intsetFind(my_ints, 100));

    return 0;
}

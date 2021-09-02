#include <stdio.h>
#include "dict.h"
#include "intset.h"
#include "adlist.h"
#include "zipmap.h"
#include "ziplist.h"
#include "sds.h"

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
    printf("intset: %d\n", intsetFind(my_ints, 97));
    printf("intset: %d\n", intsetFind(my_ints, 100));

    // 双端链表
    list *my_list = listCreate();
    listAddNodeHead(my_list, arr[3]);
    listAddNodeTail(my_list, arr[5]);
    listNode *my_node = listSearchKey(my_list, arr[3]);
    listIter *my_iter = listGetIterator(my_list, 1);
    listInsertNode(my_list, my_node, arr[4], 1);
    while (my_node = listNext(my_iter)) {
        printf("list: %s\n", my_node->value);
    }

    // zipmap
    int update, vlen;
    unsigned char *my_zm = zipmapNew();
    unsigned char *value;
    zipmapSet(my_zm, arr[0], 4, arr[3], 4, &update);
    zipmapSet(my_zm, arr[0], 4, arr[4], 4, &update);
    zipmapGet(my_zm, arr[0], 4, &value, &vlen);
    printf("zipmap: %s vlen: %d update: %d\n", value, vlen, update);

    // ziplist
    unsigned char *my_zl = ziplistNew();
    ziplistPush(my_zl, arr[3], 4, ZIPLIST_HEAD);
    ziplistPush(my_zl, arr[4], 4, ZIPLIST_HEAD);
    printf("ziplist: %s\n", ziplistIndex(my_zl, 1));

    // sds
    sds my_empty = sdsempty();
    sds my_new = sdsnew(arr[3]);
    sds my_newlen = sdsnewlen(arr[4], 20);
    my_empty = sdsdup(my_new);
    printf("sds my_empty: %s\n", my_empty);
    printf("sds my_new: %s\n", my_new);
    printf("sds my_newlen: %s\n", my_newlen);

    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

struct TreeNode *newNode(int val, struct TreeNode *left, struct TreeNode *right) {
    struct TreeNode *obj = (struct TreeNode *) malloc(sizeof(struct TreeNode));
    obj->val = val;
    obj->left = left;
    obj->right = right;
    return obj;
}

int maxSubArray(int* nums, int numsSize) {
    int *f = (int *)malloc(sizeof(int) * numsSize);
    memset(f, 0, sizeof(int) * numsSize);
    f[0] = nums[0];
    int sum = f[0];
    for (int i = 1; i < numsSize; i++) {
        if (f[i - 1] > 0) {
            f[i] = f[i - 1] + nums[i];
        } else {
            f[i] = nums[i];
        }
        if (f[i] > sum) {
            sum = f[i];
        }
    }
    return sum;
}

int main(int argc, char *argv[]) {
    struct TreeNode *a = newNode(1, newNode(2, 0, 0), newNode(3, newNode(4, 0, 0), newNode(5, 0, 0)));

    int nums[5] = {5,4,2,4,1};


    printf("%d\n", maxSubArray(nums, 5));

    return 0;
}

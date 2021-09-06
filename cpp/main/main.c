#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

int partition(int *nums, int p, int r, int *len) {
    int q = p;
    int value = nums[p];
    for (int i = p + 1; i <= r; i++) {
        if (nums[i] <= value) {
            nums[q] = nums[i];
            q++;
            nums[i] = nums[q];
        }
    }
    nums[q] = value;

    // 相等的排在一起
    int equalTemp, equalQ = 0;
    for (int i = 0; i < q; i++) {
        if (nums[i] < value) {
            equalTemp = nums[i];
            nums[i] = nums[equalQ];
            nums[equalQ] = equalTemp;
            equalQ++;
        } else {
            *len = *len + 1;
        }
    }
    return q;
}

void quickSort(int *nums, int p, int r) {
    if (r <= p) {
        return;
    }
    int len = 0;
    int q = partition(nums, p, r, &len);
    quickSort(nums, q + 1, r);
    quickSort(nums, p, q - len);
}

int majorityElement(int *nums, int numsSize) {
    quickSort(nums, 0, numsSize - 1);
    int half = numsSize / 2;
    int isOdd = numsSize % 2;
    if (!isOdd && nums[half] != nums[numsSize - 1]) {
        return half > 0 ? nums[half - 1] : nums[0];
    } else {
        return nums[half];
    }
}

int main(int argc, char *argv[]) {
    int arr[] = {12, 52, 12, 70, 12, 61, 12, 12, 50, 72, 82, 12, 11, 25, 28, 43, 40, 12, 12, 53, 12, 12, 98, 12, 12, 92,
                 81, 2, 12, 15, 40, 12, 12, 9, 12, 31, 12, 12, 12, 12, 77, 12, 12, 50, 12, 12, 12, 93, 41, 92, 12, 12,
                 12, 12, 12, 12, 12, 12, 12, 37, 48, 14, 12, 70, 82, 12, 80, 12, 12, 12, 12, 56, 30, 12, 8, 12, 50, 12,
                 20, 12, 21, 97, 12, 42, 12, 10, 12, 38, 73, 15, 9, 11, 79, 12, 12, 28, 51, 12, 15, 12};
    int num = sizeof(arr) / sizeof(int);
    int re = majorityElement(arr, num);
    printf("%d \n", re);
    return 0;
}

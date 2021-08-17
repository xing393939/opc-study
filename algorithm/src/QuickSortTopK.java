import java.util.Arrays;

// 利用快排算法，查找第K大的元素，时间复杂度是O(n)
public class QuickSortTopK {

    // 快速排序，A是数组，n表示数组的大小
    public void quick_sort_top_k(int[] A, int k) {
        quick_sort_c(A, 0, A.length - 1, k);
    }

    // 快速排序递归函数，p,r为下标
    private void quick_sort_c(int[] A, int p, int r, int k) {
        if (p >= r) return;

        int q = partition(A, p, r);
        if (q > k) {
            quick_sort_c(A, p, q - 1, k);
        } else if (q < k) {
            quick_sort_c(A, q + 1, r, k);
        }
    }

    private int partition(int[] A, int p, int r) {
        int pivot = A[r], i = p, j = p, tmp;
        for (; j <= r - 1; j++) {
            if (A[j] > pivot) {
                tmp = A[i];
                A[i] = A[j];
                A[j] = tmp;
                i++;
            }
        }
        tmp = A[i];
        A[i] = A[j];
        A[j] = tmp;
        return i;
    }

    public static void main(String[] args) {
        int A[] = new int[]{5, 2, 7, 4, 1, 6, 3, 8};
        QuickSortTopK tool = new QuickSortTopK();
        System.out.println(Arrays.toString(A));

        int k = 4;
        tool.quick_sort_top_k(A, k - 1);
        System.out.println(A[k - 1]);
    }
}

import java.util.Arrays;

public class QuickSort {

    // 快速排序，A是数组，n表示数组的大小
    public void quick_sort(int[] A, int n) {
        quick_sort_c(A, 0, n - 1);
    }

    // 快速排序递归函数，p,r为下标
    private void quick_sort_c(int[] A, int p, int r) {
        if (p >= r) return;

        int q = partition(A, p, r);
        quick_sort_c(A, p, q - 1);
        quick_sort_c(A, q + 1, r);
    }

    private int partition(int[] A, int p, int r) {
        int pivot = A[r], i = p, j = p, tmp;
        for (; j <= r - 1; j++) {
            if (A[j] < pivot) {
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
        QuickSort tool = new QuickSort();
        System.out.println(Arrays.toString(A));
        tool.quick_sort(A, 8);
        System.out.println(Arrays.toString(A));
    }
}

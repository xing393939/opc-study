import java.util.Arrays;

public class MergeSort {

    // 归并排序算法, A是数组，n表示数组大小
    public void merge_sort(int[] A, int n) {
        merge_sort_c(A, 0, n - 1);
    }

    // 递归调用函数
    private void merge_sort_c(int[] A, int p, int r) {
        // 递归终止条件
        if (p >= r) return;
        // 取p到r之间的中间位置q
        int q = (p + r) / 2;
        // 分治递归
        merge_sort_c(A, p, q);
        merge_sort_c(A, q + 1, r);
        merge(A, p, r, q);
    }

    private void merge(int[] A, int p, int r, int q) {
        int i = p, j = q + 1, k = 0;
        int tmp[] = new int[r - p + 1];
        while (i <= q && j <= r) {
            if (A[i] <= A[j]) {
                tmp[k++] = A[i++];
            } else {
                tmp[k++] = A[j++];
            }
        }

        // 判断哪个子数组中有剩余的数据
        int start = i, end = q;
        if (j <= r) {
            start = j;
            end = r;
        }

        // 将剩余的数据拷贝到临时数组tmp
        while (start <= end) {
            tmp[k++] = A[start++];
        }

        // 将tmp中的数组拷贝回A[p...r]
        for (i = 0; i <= r - p; i++) {
            A[p + i] = tmp[i];
        }
    }

    public static void main(String[] args) {
        int A[] = new int[]{5, 2, 7, 4, 1, 6, 3, 8};
        MergeSort tool = new MergeSort();
        System.out.println(Arrays.toString(A));
        tool.merge_sort(A, 8);
        System.out.println(Arrays.toString(A));
    }
}

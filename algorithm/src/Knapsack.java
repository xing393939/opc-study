public class Knapsack {

    public static int maxW = Integer.MIN_VALUE; //存储背包中物品总重量的最大值

    /*
     * i表示考察到哪个物品了；
     * cw表示当前已经装进去的物品的重量和；
     * items表示每个物品的重量；
     * n表示物品个数；
     * w背包重量；
     */
    public static void f(int i, int cw, int[] items, int n, int w) {
        if (cw == w || i == n) { // cw==w表示装满了;i==n表示已经考察完所有的物品
            if (cw > maxW) maxW = cw;
            System.out.printf("%d %d return \n", i, cw);
            return;
        }
        System.out.printf("%d %d \n", i, cw);

        f(i + 1, cw, items, n, w);
        if (cw + items[i] <= w) {// 已经超过可以背包承受的重量的时候，就不要再装了
            f(i + 1, cw + items[i], items, n, w);
        }
    }

    public static void main(String[] args) {
        // 假设背包可承受重量100，物品个数10
        int items[] = new int[]{10, 22, 7, 44, 9, 66, 5, 33, 8, 11};
        f(0, 0, items, 10, 100);
        System.out.println(maxW);
    }
}

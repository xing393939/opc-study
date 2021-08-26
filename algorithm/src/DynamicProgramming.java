public class DynamicProgramming {

    public static int getFibonacci1(int n) {
        if (n == 0) {
            return 0;
        } else if (n == 1) {
            return 1;
        } else {
            return getFibonacci1(n - 1) + getFibonacci1(n - 2);
        }
    }

    public static int getFibonacci2(int n) {
        int[] arr = new int[n + 1];
        arr[0] = 0;
        arr[1] = 1;
        for (int i = 2; i <= n; i++) {
            arr[i] = arr[i - 1] + arr[i - 2];
        }
        return arr[n];
    }

    public static int getBestGoldMining1(int workers, int miningCount, int[] people, int[] mining) {
        if (workers <= 0 || miningCount <= 0) return 0;

        int c = miningCount - 1;
        if (workers < people[c]) {
            return getBestGoldMining1(workers, c, people, mining);
        }

        return Math.max(getBestGoldMining1(workers, c, people, mining),
                getBestGoldMining1(workers - people[c], c, people, mining) + mining[c]);
    }

    public static int getBestGoldMining2(int workers, int miningCount, int[] people, int[] mining) {
        int best = 0;
        int[] prevLine = new int[workers + 1];
        int[] currLine = new int[workers + 1];
        for (int i = 1; i <= miningCount; i++) {
            for (int j = 1; j <= workers; j++) {
                if (j >= people[i - 1]) {
                    currLine[j] = Math.max(prevLine[j], prevLine[j - people[i - 1]] + mining[i - 1]);
                    best = Math.max(currLine[j], best);
                }
            }
            prevLine = currLine.clone();
        }
        return best;
    }

    public static int getMoneyN1(int money) {
        if (money < 0) {
            return Integer.MAX_VALUE;
        }
        if (money == 0) {
            return 0;
        }
        return Math.min(Math.min(getMoneyN1(money - 1), getMoneyN1(money - 3)), getMoneyN1(money - 5)) + 1;
    }

    // 传参money必定>=5
    public static int getMoneyN2(int money) {
        int[] prevLine = new int[money + 1];
        int[] currLine = new int[money + 1];
        for (int i = 0; i <= money; i++) {
            prevLine[i] = Integer.MAX_VALUE;
            currLine[i] = Integer.MAX_VALUE;
        }
        prevLine[1] = 1;
        prevLine[3] = 1;
        prevLine[5] = 1;
        // 最多求解到10000个硬币
        for (int n = 2; n < 10000; n++) {
            for (int i = 5; i <= money; i++) {
                int best = 1 + Math.min(Math.min(prevLine[i - 1], prevLine[i - 3]), prevLine[i - 5]);
                if (best > 0) {
                    if (i == money) {
                        return n;
                    }
                    currLine[i] = best;
                }
            }
            prevLine = currLine.clone();
        }
        return -1;
    }

    public static void main(String[] args) {
        // 斐波那契数列
        System.out.println(getFibonacci1(10));
        System.out.println(getFibonacci2(10));

        // 国王和金矿
        int workers = 10;
        int[] people = {5, 5, 3, 4, 3};
        int[] mining = {400, 500, 200, 300, 350};
        System.out.println(getBestGoldMining1(workers, mining.length, people, mining));
        System.out.println(getBestGoldMining2(workers, mining.length, people, mining));

        // 支付9元最少需要几个钱币（钱币有1、3、5）
        System.out.println(getMoneyN1(9));
        System.out.println(getMoneyN2(9));
    }
}

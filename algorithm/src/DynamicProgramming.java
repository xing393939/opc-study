public class DynamicProgramming {

    public static int getBestGoldMining(int workers, int miningCount, int[] people, int[] mining) {
        if (workers <= 0 || miningCount <= 0) return 0;

        int c = miningCount - 1;
        if (workers < people[c]) {
            return getBestGoldMining(workers, c, people, mining);
        }

        return Math.max(getBestGoldMining(workers, c, people, mining),
                getBestGoldMining(workers - people[c], c, people, mining) + mining[c]);
    }

    public static void main(String[] args) {
        int workers = 10;
        int[] people = {5, 5, 3, 4, 3};
        int[] mining = {400, 500, 200, 300, 350};
        System.out.println(getBestGoldMining(workers, mining.length, people, mining));
    }
}

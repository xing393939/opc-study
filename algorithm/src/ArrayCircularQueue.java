// 相比ArrayQueue，当enqueue到数组最后一个元素时，不需要搬迁数据
public class ArrayCircularQueue {
    // 数组：items，数组大小：n
    private String[] items;
    private int n = 0;
    // head表示队头下标，tail表示队尾下标
    private int head = 0;
    private int tail = 0;

    // 申请一个大小为capacity的数组
    public ArrayCircularQueue(int capacity) {
        items = new String[capacity];
        n = capacity;
    }

    // 入队
    public boolean enqueue(String item) {
        // 队列满了
        if ((tail + 1) % n == head) return false;
        items[tail] = item;
        tail = (tail + 1) % n;
        return true;
    }

    // 出队
    public String dequeue() {
        // 如果head == tail 表示队列为空
        if (head == tail) return null;
        String ret = items[head];
        head = (head + 1) % n;
        return ret;
    }

    public static void main(String[] args) {
        ArrayCircularQueue queue = new ArrayCircularQueue(1000);
        queue.enqueue("1");
        queue.enqueue("2");
        System.out.println(queue.dequeue());
    }
}

public class SingleLinkedList {

    private static class Node {
        private int value;
        private Node next;

        private Node(int val, Node node) {
            value = val;
            next = node;
        }
    }

    public static Node initHeadNode(int val) {
        return new Node(-1, new Node(val, null));
    }

    public static Node[] find(Node head, int val) {
        Node curr = null;
        Node prev = head;
        while (prev != null) {
            if (prev.next != null && prev.next.value == val) {
                curr = prev.next;
                break;
            }
            prev = prev.next;
        }

        return new Node[]{prev, curr};
    }

    public static void insertAfter(Node head, int val, int newVal) {
        Node temp[] = find(head, val);
        if (temp[1] != null) {
            Node newNode = new Node(newVal, temp[1].next);
            temp[1].next = newNode;
        }
    }

    public static void insertBefore(Node head, int val, int newVal) {
        Node temp[] = find(head, val);
        if (temp[1] != null) {
            Node newNode = new Node(newVal, temp[1]);
            temp[0].next = newNode;
        }
    }

    public static void delete(Node head, int val) {
        Node temp[] = find(head, val);
        if (temp[1] != null) {
            temp[0].next = temp[1].next;
        }
    }

    public static void print(Node head) {
        Node temp = head.next;
        for (; temp != null; temp = temp.next) {
            System.out.println(temp.value);
        }
    }

    public static void main(String[] args) {
        Node head = initHeadNode(1);
        insertAfter(head, 1, 2);
        insertAfter(head, 1, 3);
        insertBefore(head, 2, 4);
        print(head);
        delete(head, 1);
        print(head);
    }
}

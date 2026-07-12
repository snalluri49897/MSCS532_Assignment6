# stack (LIFO), backed by a fixed-size array
class Stack:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1  # -1 means empty

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.capacity - 1

    def push(self, value):
        if self.is_full():
            raise OverflowError("Stack overflow")
        self.top += 1
        self.data[self.top] = value

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack underflow")
        value = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.data[self.top]


# queue (FIFO), backed by a circular buffer so we don't shift elements around
class Queue:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.data = [None] * capacity
        self.head = 0   # index of the front element
        self.size = 0    # how many elements are currently stored

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, value):
        if self.is_full():
            raise OverflowError("Queue overflow")
        tail = (self.head + self.size) % self.capacity
        self.data[tail] = value
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue underflow")
        value = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.data[self.head]


# singly linked list node
class SLLNode:
    def __init__(self, value):
        self.value = value
        self.next = None


# singly linked list, insert at head is O(1), search/delete are O(n)
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, value):
        node = SLLNode(value)
        node.next = self.head
        self.head = node

    def search(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete(self, value):
        current = self.head
        previous = None
        while current is not None:
            if current.value == value:
                if previous is None:
                    self.head = current.next  # deleting the head
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False  # value wasn't in the list

    def to_list(self):
        # just for testing/printing
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


# doubly linked list node, has a prev pointer too
class DLLNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


# doubly linked list, lets us delete in O(1) once we already have the node
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_head(self, value):
        node = DLLNode(value)
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node

    def insert_at_tail(self, value):
        node = DLLNode(value)
        node.prev = self.tail
        if self.tail is not None:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node

    def search(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete_node(self, node):
        # O(1) since we already have the node, no need to scan for "previous"
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next  # node was the head

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # node was the tail

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


# basic sanity tests
if __name__ == "__main__":
    # stack test
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.peek() == 2
    print("Stack OK")

    # queue test
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    assert q.dequeue() == "a"
    assert q.peek() == "b"
    print("Queue OK")

    # singly linked list test
    sll = SinglyLinkedList()
    sll.insert_at_head(3)
    sll.insert_at_head(2)
    sll.insert_at_head(1)
    assert sll.to_list() == [1, 2, 3]
    assert sll.search(2) is not None
    sll.delete(2)
    assert sll.to_list() == [1, 3]
    print("Singly Linked List OK")

    # doubly linked list test
    dll = DoublyLinkedList()
    dll.insert_at_tail(1)
    dll.insert_at_tail(2)
    dll.insert_at_tail(3)
    assert dll.to_list() == [1, 2, 3]
    middle_node = dll.search(2)
    dll.delete_node(middle_node)
    assert dll.to_list() == [1, 3]
    print("Doubly Linked List OK")

    print("\nAll Part 2 tests passed.")
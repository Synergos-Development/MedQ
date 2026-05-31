class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

    def display(self):
        current = self.head

        print("Riwayat Pasien:")

        while current:
            print(current.data, end=" -> ")
            current = current.next

        print("None")


if __name__ == "__main__":
    pasien = LinkedList()

    pasien.append("Kunjungan 1")
    pasien.append("Kunjungan 2")
    pasien.append("Kunjungan 3")

    pasien.display()
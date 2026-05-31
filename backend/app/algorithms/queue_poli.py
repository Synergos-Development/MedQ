class QueuePoli:
    def __init__(self):
        self.queue = []

    def enqueue(self, pasien):
        self.queue.append(pasien)
        print(f"{pasien} masuk antrian")

    def dequeue(self):
        if self.is_empty():
            print("Antrian kosong")
            return None

        pasien = self.queue.pop(0)
        print(f"{pasien} dipanggil")
        return pasien

    def front(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        print("Isi antrian:")
        for pasien in self.queue:
            print("-", pasien)


if __name__ == "__main__":
    poli = QueuePoli()

    poli.enqueue("Pasien A")
    poli.enqueue("Pasien B")
    poli.enqueue("Pasien C")

    poli.display()

    poli.dequeue()

    poli.display()
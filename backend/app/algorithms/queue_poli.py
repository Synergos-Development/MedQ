"""
queue_poli.py

Implementasi Queue FIFO per Poli menggunakan Linked List.

Konsep:
- Setiap poli memiliki queue sendiri.
- Pasien masuk dari belakang (enqueue).
- Pasien keluar dari depan (dequeue).
- Nomor antrian dibuat berdasarkan kode poli dan urutan harian.

Contoh:
    UMUM-001
    GIGI-005
    JANTUNG-002

Kompleksitas:
- enqueue    : O(1)
- dequeue    : O(1)
- get_posisi : O(n)
"""

import logging
from datetime import date

logger = logging.getLogger(__name__)


class Node:
    """Node internal untuk Queue."""

    def __init__(self, id_antrian: int, nomor_antrian: str):
        self.id_antrian = id_antrian
        self.nomor_antrian = nomor_antrian
        self.next = None


class QueuePoli:
    """
    Queue FIFO untuk satu poli.

    Menggunakan linked list agar enqueue dan dequeue
    tetap O(1).
    """

    def __init__(self, kode_poli: str):
        self.kode_poli = kode_poli

        self.head = None
        self.tail = None
        self.size = 0

        self._counter = 0
        self._tanggal_init = date.today()

    def _reset_jika_hari_baru(self):
        """Reset queue dan counter jika hari berganti."""
        if date.today() != self._tanggal_init:
            self._counter = 0
            self._tanggal_init = date.today()
 
            self.head = None
            self.tail = None
            self.size = 0
 
    def _parse_counter_from_nomor(self, nomor_antrian: str) -> int:
        """Parse counter dari nomor antrian yang valid untuk restore."""
        if not isinstance(nomor_antrian, str):
            return 0
 
        try:
            prefix, suffix = nomor_antrian.rsplit('-', 1)
            if prefix != self.kode_poli:
                raise ValueError('prefix mismatch')
 
            return int(suffix)
        except Exception as exc:
            logger.warning(
                "Nomor antrian tidak valid saat restore untuk poli %s: %s (%s)",
                self.kode_poli,
                nomor_antrian,
                exc,
            )
            return 0

    def generate_nomor(self) -> str:
        """
        Generate nomor antrian berikutnya.

        Returns:
            str
        """
        self._reset_jika_hari_baru()

        self._counter += 1

        return (
            f"{self.kode_poli}-"
            f"{str(self._counter).zfill(3)}"
        )

    def enqueue(self, id_antrian: int, nomor_antrian: str):
        """
        Tambahkan pasien ke belakang antrian.
        """
        node = Node(id_antrian, nomor_antrian)

        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.size += 1

    def dequeue(self):
        """
        Keluarkan pasien paling depan.

        Returns:
            tuple(id_antrian, nomor_antrian) atau None
        """
        if self.head is None:
            return None

        node = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        self.size -= 1

        return (
            node.id_antrian,
            node.nomor_antrian
        )

    def peek(self):
        """
        Lihat pasien paling depan tanpa mengeluarkan.

        Returns:
            tuple(id_antrian, nomor_antrian) atau None
        """
        if self.head is None:
            return None

        return (
            self.head.id_antrian,
            self.head.nomor_antrian
        )

    def get_posisi(self, id_antrian: int) -> int:
        """
        Cari posisi pasien dalam antrian.

        Returns:
            posisi (mulai dari 1) atau 0 jika tidak ditemukan.
        """
        posisi = 1
        current = self.head

        while current:
            if current.id_antrian == id_antrian:
                return posisi

            current = current.next
            posisi += 1

        return 0

    def remove(self, id_antrian: int) -> bool:
        """
        Hapus pasien tertentu dari antrian.

        Returns:
            bool
        """
        if self.head is None:
            return False

        if self.head.id_antrian == id_antrian:
            self.head = self.head.next

            if self.head is None:
                self.tail = None

            self.size -= 1
            return True

        current = self.head

        while current.next:
            if current.next.id_antrian == id_antrian:

                if current.next == self.tail:
                    self.tail = current

                current.next = current.next.next

                self.size -= 1
                return True

            current = current.next

        return False

    def is_empty(self) -> bool:
        """Cek apakah queue kosong."""
        return self.size == 0

    def to_list(self) -> list:
        """
        Konversi seluruh antrian menjadi list.
        """
        hasil = []
        current = self.head

        while current:
            hasil.append({
                "id_antrian": current.id_antrian,
                "nomor_antrian": current.nomor_antrian,
            })

            current = current.next

        return hasil

    def __len__(self):
        return self.size

    def __repr__(self):
        items = [
            item["nomor_antrian"]
            for item in self.to_list()
        ]

        return (
            f"QueuePoli({self.kode_poli}): "
            f"[{' -> '.join(items)}]"
        )


class QueueManager:
    """
    Mengelola queue untuk seluruh poli.
    """

    def __init__(self):
        self._queues: dict[int, QueuePoli] = {}

    def _get_queue(
        self,
        id_poli: int,
        kode_poli: str = ''
    ) -> QueuePoli:

        if id_poli not in self._queues:
            self._queues[id_poli] = QueuePoli(kode_poli)

        return self._queues[id_poli]

    def generate_nomor(
        self,
        kode_poli: str,
        id_poli: int
    ) -> str:

        queue = self._get_queue(
            id_poli,
            kode_poli
        )

        return queue.generate_nomor()

    def enqueue(
        self,
        id_poli: int,
        id_antrian: int,
        nomor_antrian: str
    ):
        queue = self._get_queue(id_poli)
        queue.enqueue(id_antrian, nomor_antrian)

    def dequeue(self, id_poli: int):
        queue = self._get_queue(id_poli)
        return queue.dequeue()

    def get_posisi(
        self,
        id_poli: int,
        id_antrian: int
    ) -> int:

        queue = self._get_queue(id_poli)
        return queue.get_posisi(id_antrian)

    def remove(
        self,
        id_poli: int,
        id_antrian: int
    ) -> bool:

        queue = self._get_queue(id_poli)
        return queue.remove(id_antrian)

    def get_semua_antrian(
        self,
        id_poli: int
    ) -> list:

        queue = self._get_queue(id_poli)
        return queue.to_list()

    def restore_queue(
        self,
        active_antrian
    ):
        """
        Restore queue dan counter dari database.
        """

        self._queues.clear()

        for antrian in active_antrian:

            queue = self._get_queue(
                antrian.id_poli,
                antrian.poli.kode_poli
            )

            queue.enqueue(
                antrian.id_antrian,
                antrian.nomor_antrian
            )

            counter = queue._parse_counter_from_nomor(
                antrian.nomor_antrian
            )

            if counter > queue._counter:
                queue._counter = counter

        logger.info(
            "Queue recovery selesai. Total poli: %s",
            len(self._queues)
        )
        
        for id_poli, queue in self._queues.items():
            logger.info(
                "POLI=%s SIZE=%s DATA=%s",
                id_poli,
                len(queue),
                queue.to_list()
            )


# Instance global
queue_manager = QueueManager()
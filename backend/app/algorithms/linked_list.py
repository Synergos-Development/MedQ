"""
linked_list.py

Implementasi Linked List untuk riwayat kunjungan pasien.

Setiap pasien memiliki linked list sendiri yang menyimpan
riwayat kunjungan secara berurutan dari yang terbaru (head)
hingga yang terlama (tail).

Kompleksitas:
- insert    : O(1)
- traversal : O(n)
- search    : O(n)
"""


class KunjunganNode:
    """Node yang menyimpan satu data kunjungan."""

    def __init__(self, data: dict):
        self.data = data
        self.next = None


class RiwayatLinkedList:
    """
    Linked List riwayat kunjungan untuk satu pasien.

    Kunjungan terbaru selalu berada di head.
    """

    def __init__(self, id_pasien: int):
        self.id_pasien = id_pasien
        self.head = None
        self.size = 0

    def tambah_kunjungan(self, data: dict):
        """
        Menambahkan kunjungan baru ke depan list.

        Args:
            data: dictionary detail kunjungan
        """
        node = KunjunganNode(data)
        node.next = self.head
        self.head = node
        self.size += 1

    def get_semua(self) -> list:
        """
        Mengambil seluruh riwayat kunjungan.

        Returns:
            list data kunjungan (terbaru → terlama)
        """
        hasil = []
        current = self.head

        while current:
            hasil.append(current.data)
            current = current.next

        return hasil

    def get_kunjungan_terakhir(self) -> dict | None:
        """
        Mengambil kunjungan terbaru pasien.

        Returns:
            dict kunjungan atau None
        """
        return self.head.data if self.head else None

    def cari_by_id(self, id_kunjungan: int) -> dict | None:
        """
        Mencari kunjungan berdasarkan ID.

        Args:
            id_kunjungan: ID kunjungan

        Returns:
            dict kunjungan atau None
        """
        current = self.head

        while current:
            if current.data.get("id_kunjungan") == id_kunjungan:
                return current.data

            current = current.next

        return None

    def cari_by_poli(self, nama_poli: str) -> list:
        """
        Mencari seluruh kunjungan pada poli tertentu.

        Args:
            nama_poli: nama poli

        Returns:
            list kunjungan yang cocok
        """
        hasil = []
        current = self.head

        while current:
            if current.data.get("nama_poli", "").lower() == nama_poli.lower():
                hasil.append(current.data)

            current = current.next

        return hasil

    def is_empty(self) -> bool:
        """Mengembalikan True jika riwayat kosong."""
        return self.head is None

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        items = [
            str(node.get("id_kunjungan", "?"))
            for node in self.get_semua()
        ]

        return (
            f"RiwayatLinkedList(pasien={self.id_pasien}): "
            f"[{' → '.join(items)}]"
        )


class RiwayatManager:
    """
    Mengelola seluruh riwayat kunjungan pasien.

    Mapping:
        id_pasien -> RiwayatLinkedList
    """

    def __init__(self):
        self._riwayat: dict[int, RiwayatLinkedList] = {}

    def _get_list(self, id_pasien: int) -> RiwayatLinkedList:
        """
        Mengambil linked list pasien.

        Jika belum ada maka dibuat otomatis.
        """
        if id_pasien not in self._riwayat:
            self._riwayat[id_pasien] = RiwayatLinkedList(id_pasien)

        return self._riwayat[id_pasien]

    def tambah(self, id_pasien: int, data: dict):
        """Menambahkan kunjungan baru."""
        self._get_list(id_pasien).tambah_kunjungan(data)

    def get_semua(self, id_pasien: int) -> list:
        """Mengambil seluruh riwayat pasien."""
        return self._get_list(id_pasien).get_semua()

    def get_terakhir(self, id_pasien: int) -> dict | None:
        """Mengambil kunjungan terakhir pasien."""
        return self._get_list(id_pasien).get_kunjungan_terakhir()

    def cari(self, id_pasien: int, id_kunjungan: int) -> dict | None:
        """Mencari kunjungan pasien berdasarkan ID."""
        return self._get_list(id_pasien).cari_by_id(id_kunjungan)


# Instance global untuk digunakan oleh service
riwayat_manager = RiwayatManager()
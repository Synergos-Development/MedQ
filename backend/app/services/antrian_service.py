from app.algorithms.queue_poli import QueuePoli

#queues
# simpan antrean tiap poli

#enqueue()
# tambah antrean

#dequeue()
# ambil pasien paling depan

#staticmethod
# fungsi bisa dipanggil tanpa bikin object


# simpan queue per poli
queues = {
    "umum": QueuePoli(),
    "gigi": QueuePoli(),
    "anak": QueuePoli()
}


class AntreanService:

    @staticmethod
    def tambah_antrian(rm, poli):

        queue = queues[poli]

        nomor = queue.enqueue(
            rm
        )

        return {
            "message": "berhasil",
            "nomor": nomor,
            "poli": poli
        }

    @staticmethod
    def next_queue(poli):

        queue = queues[poli]

        pasien = queue.dequeue()

        return {
            "dipanggil": pasien
        }

    @staticmethod
    def get_queue(poli):

        queue = queues[poli]

        return queue.items
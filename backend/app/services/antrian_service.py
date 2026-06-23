from app import db
from app.models.antrian import Antrian
from app.models.poli import Poli, Dokter
from app.algorithms.queue_poli import queue_manager
from datetime import datetime, date


class AntrianService:

    @staticmethod
    def ambil_nomor(id_pasien, id_poli, id_dokter):
        """
        Pasien mengambil nomor antrian.
        Returns: (antrian, error)
        """
        # Validasi poli dan dokter
        poli   = Poli.query.get(id_poli)
        dokter = Dokter.query.get(id_dokter)
        if not poli:
            return None, 'Poli tidak ditemukan.'
        if not dokter:
            return None, 'Dokter tidak ditemukan.'
        if not dokter.is_available:
            return None, 'Dokter sedang tidak tersedia.'

        # Cek apakah pasien sudah punya antrian aktif hari ini di poli yang sama
        antrian_aktif = Antrian.query.filter_by(
            id_pasien = id_pasien,
            id_poli   = id_poli,
            tanggal   = date.today(),
        ).filter(Antrian.status.in_(['Menunggu', 'Dipanggil', 'Diperiksa'])).first()

        if antrian_aktif:
            return None, f'Kamu sudah memiliki antrian aktif: {antrian_aktif.nomor_antrian}'

        # Generate nomor antrian via Queue algorithm
        nomor_antrian = queue_manager.generate_nomor(poli.kode_poli, id_poli)

        # Simpan ke database
        antrian = Antrian(
            nomor_antrian = nomor_antrian,
            id_pasien     = id_pasien,
            id_poli       = id_poli,
            id_dokter     = id_dokter,
            tanggal       = date.today(),
            status        = 'Menunggu',
        )
        db.session.add(antrian)
        db.session.commit()

        # Masukkan ke queue in-memory
        queue_manager.enqueue(id_poli, antrian.id_antrian, nomor_antrian)

        # Hitung posisi dan estimasi
        posisi  = queue_manager.get_posisi(id_poli, antrian.id_antrian)
        estimasi = posisi * 10  # estimasi 10 menit per pasien

        return {
            'id_antrian':    antrian.id_antrian,
            'nomor_antrian': nomor_antrian,
            'nama_poli':     poli.nama_poli,
            'nama_dokter':   dokter.nama_dokter,
            'posisi':        posisi,
            'estimasi_menit': estimasi,
        }, None

    @staticmethod
    def cek_status(nomor_antrian):
        """
        Cek status antrian berdasarkan nomor antrian.
        Returns: (data, error)
        """
        antrian = Antrian.query.filter_by(nomor_antrian=nomor_antrian).first()
        if not antrian:
            return None, 'Nomor antrian tidak ditemukan.'

        posisi   = queue_manager.get_posisi(antrian.id_poli, antrian.id_antrian)
        estimasi = posisi * 10

        return {
            'nomor_antrian':  antrian.nomor_antrian,
            'status':         antrian.status,
            'posisi':         posisi,
            'estimasi_menit': estimasi,
        }, None

    @staticmethod
    def panggil_berikutnya(id_poli, id_dokter):
        """
        Admin/dokter memanggil nomor antrian berikutnya (FIFO).
        Returns: (data, error)
        """
        # Ambil nomor berikutnya dari queue in-memory
        next_item = queue_manager.dequeue(id_poli)
        if not next_item:
            return None, 'Tidak ada antrian yang menunggu.'

        id_antrian, nomor_antrian = next_item

        # Update status di database
        antrian = Antrian.query.get(id_antrian)
        if not antrian:
            # Fallback: ambil dari database langsung
            antrian = Antrian.query.filter_by(
                id_poli = id_poli,
                status  = 'Menunggu',
                tanggal = date.today(),
            ).order_by(Antrian.waktu_daftar.asc()).first()

            if not antrian:
                return None, 'Tidak ada antrian yang menunggu.'

        antrian.status          = 'Dipanggil'
        antrian.waktu_dipanggil = datetime.now()
        db.session.commit()

        from app.models.pasien import Pasien
        pasien = Pasien.query.get(antrian.id_pasien)

        return {
            'nomor_antrian': antrian.nomor_antrian,
            'nama_pasien':   pasien.nama_lengkap if pasien else '-',
            'id_antrian':    antrian.id_antrian,
        }, None

    @staticmethod
    def batalkan(id_antrian):
        """
        Batalkan antrian pasien.
        Returns: (pesan, error)
        """
        antrian = Antrian.query.get(id_antrian)
        if not antrian:
            return None, 'Antrian tidak ditemukan.'
        if antrian.status in ['Selesai', 'Batal']:
            return None, f'Antrian sudah berstatus {antrian.status}.'

        antrian.status = 'Batal'
        db.session.commit()

        # Hapus dari queue in-memory
        queue_manager.remove(antrian.id_poli, id_antrian)

        return f'Antrian {antrian.nomor_antrian} berhasil dibatalkan.', None

    @staticmethod
    def get_antrian_aktif(id_poli):
        """
        Ambil data antrian aktif untuk layar display.
        Returns: (data, error)
        """
        # Sedang dilayani
        dilayani = Antrian.query.filter_by(
            id_poli = id_poli,
            tanggal = date.today(),
            status  = 'Dipanggil',
        ).order_by(Antrian.waktu_dipanggil.desc()).first()

        # Antrian menunggu
        menunggu = Antrian.query.filter_by(
            id_poli = id_poli,
            tanggal = date.today(),
            status  = 'Menunggu',
        ).order_by(Antrian.waktu_daftar.asc()).all()

        return {
            'sedang_dilayani':  dilayani.nomor_antrian if dilayani else None,
            'antrian_menunggu': [a.nomor_antrian for a in menunggu],
            'total_menunggu':   len(menunggu),
        }, None
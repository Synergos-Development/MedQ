from app import db
from app.models.pasien import Pasien
from app.algorithms.hash_rm import generate_nomor_rm
from datetime import datetime

class PendaftaranService:

    @staticmethod
    def daftar_pasien_baru(data):
        """
        Mendaftarkan pasien baru dan generate nomor RM.
        Returns: (pasien, error)
        """
        # Cek apakah NIK sudah terdaftar
        existing = Pasien.query.filter_by(nik=data['nik']).first()
        if existing:
            return None, 'NIK sudah terdaftar. Gunakan alur pasien lama.'

        # Generate nomor RM unik menggunakan hashing
        nomor_rm = generate_nomor_rm()

        # Buat objek pasien baru
        pasien = Pasien(
            nomor_rm      = nomor_rm,
            nama_lengkap  = data['nama_lengkap'],
            nik           = data['nik'],
            tanggal_lahir = datetime.strptime(data['tanggal_lahir'], '%Y-%m-%d').date(),
            alamat        = data.get('alamat'),
            nomor_hp      = data.get('nomor_hp'),
        )

        db.session.add(pasien)
        db.session.commit()
        return pasien, None

    @staticmethod
    def verifikasi_pasien(nomor_rm):
        """
        Verifikasi pasien lama berdasarkan nomor RM.
        Returns: (pasien, error)
        """
        pasien = Pasien.query.filter_by(nomor_rm=nomor_rm).first()
        if not pasien:
            return None, 'Nomor Rekam Medis tidak ditemukan.'
        return pasien, None

    @staticmethod
    def cari_pasien(nama):
        """
        Cari pasien berdasarkan nama (untuk admin).
        Returns: list pasien
        """
        hasil = Pasien.query.filter(
            Pasien.nama_lengkap.ilike(f'%{nama}%')
        ).limit(20).all()
        return hasil

    @staticmethod
    def get_riwayat(id_pasien):
        """
        Ambil riwayat kunjungan pasien.
        Returns: list kunjungan
        """
        from app.models.kunjungan import Kunjungan
        from app.models.antrian import Antrian
        from app.models.poli import Poli, Dokter

        riwayat = db.session.query(Kunjungan, Antrian, Poli, Dokter)\
            .join(Antrian, Kunjungan.id_antrian == Antrian.id_antrian)\
            .join(Poli,    Antrian.id_poli    == Poli.id_poli)\
            .join(Dokter,  Kunjungan.id_dokter == Dokter.id_dokter)\
            .filter(Kunjungan.id_pasien == id_pasien)\
            .order_by(Kunjungan.waktu_masuk.desc())\
            .all()

        hasil = []
        for k, a, p, d in riwayat:
            hasil.append({
                'id_kunjungan': k.id_kunjungan,
                'tanggal':      str(a.tanggal),
                'nama_poli':    p.nama_poli,
                'nama_dokter':  d.nama_dokter,
                'diagnosa':     k.diagnosa,
            })
        return hasil
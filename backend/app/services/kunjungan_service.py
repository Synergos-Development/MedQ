from app import db
from app.models.kunjungan import Kunjungan, Resep, DetailResep
from app.models.antrian import Antrian
from datetime import datetime

class KunjunganService:

    @staticmethod
    def mulai_kunjungan(id_antrian, keluhan):
        """
        Dokter memulai pemeriksaan — pasien masuk ruangan.
        Returns: (kunjungan, error)
        """
        antrian = Antrian.query.get(id_antrian)
        if not antrian:
            return None, 'Antrian tidak ditemukan.'
        if antrian.status != 'Dipanggil':
            return None, 'Pasien belum dipanggil.'

        # Update status antrian
        antrian.status = 'Diperiksa'
        db.session.commit()

        # Buat record kunjungan
        kunjungan = Kunjungan(
            id_antrian  = id_antrian,
            id_pasien   = antrian.id_pasien,
            id_dokter   = antrian.id_dokter,
            waktu_masuk = datetime.now(),
            keluhan     = keluhan,
        )
        db.session.add(kunjungan)
        db.session.commit()

        return {
            'id_kunjungan': kunjungan.id_kunjungan,
            'waktu_masuk':  str(kunjungan.waktu_masuk),
        }, None

    @staticmethod
    def selesai_kunjungan(id_kunjungan, diagnosa, catatan_dokter, resep_list):
        """
        Dokter menyelesaikan pemeriksaan, isi diagnosa dan resep.
        Returns: (data, error)
        """
        kunjungan = Kunjungan.query.get(id_kunjungan)
        if not kunjungan:
            return None, 'Kunjungan tidak ditemukan.'

        # Update kunjungan
        kunjungan.diagnosa       = diagnosa
        kunjungan.catatan_dokter = catatan_dokter
        kunjungan.waktu_keluar   = datetime.now()

        # Update status antrian jadi Selesai
        antrian        = Antrian.query.get(kunjungan.id_antrian)
        antrian.status = 'Selesai'

        id_resep = None

        # Simpan resep jika ada
        if resep_list:
            resep = Resep(id_kunjungan=id_kunjungan)
            db.session.add(resep)
            db.session.flush()  # supaya id_resep tersedia

            for item in resep_list:
                detail = DetailResep(
                    id_resep     = resep.id_resep,
                    nama_obat    = item['nama_obat'],
                    dosis        = item.get('dosis'),
                    aturan_pakai = item.get('aturan_pakai'),
                    jumlah       = item['jumlah'],
                )
                db.session.add(detail)

            id_resep = resep.id_resep

        db.session.commit()

        return {
            'id_kunjungan': id_kunjungan,
            'id_resep':     id_resep,
        }, None

    @staticmethod
    def get_detail(id_kunjungan):
        """
        Ambil detail kunjungan lengkap beserta resep.
        Returns: (data, error)
        """
        from app.models.pasien import Pasien
        from app.models.poli import Dokter

        kunjungan = Kunjungan.query.get(id_kunjungan)
        if not kunjungan:
            return None, 'Kunjungan tidak ditemukan.'

        pasien = Pasien.query.get(kunjungan.id_pasien)
        dokter = Dokter.query.get(kunjungan.id_dokter)
        resep  = kunjungan.resep

        return {
            'id_kunjungan':   kunjungan.id_kunjungan,
            'nama_pasien':    pasien.nama_lengkap if pasien else '-',
            'nama_dokter':    dokter.nama_dokter  if dokter else '-',
            'keluhan':        kunjungan.keluhan,
            'diagnosa':       kunjungan.diagnosa,
            'catatan_dokter': kunjungan.catatan_dokter,
            'waktu_masuk':    str(kunjungan.waktu_masuk)  if kunjungan.waktu_masuk  else None,
            'waktu_keluar':   str(kunjungan.waktu_keluar) if kunjungan.waktu_keluar else None,
            'resep':          resep.to_dict()['detail'] if resep else [],
        }, None
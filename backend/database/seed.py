"""
seed.py — isi data awal poli dan dokter untuk testing
Jalankan sekali: python database/seed.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.poli import Poli, Dokter, JadwalDokter
from datetime import time

app = create_app()

with app.app_context():
    # Hapus data lama (opsional, hati-hati di production)
    db.session.query(JadwalDokter).delete()
    db.session.query(Dokter).delete()
    db.session.query(Poli).delete()
    db.session.commit()

    # ── Data Poli ──────────────────────────
    poli_list = [
        Poli(kode_poli='UMUM',    nama_poli='Poli Umum'),
        Poli(kode_poli='GIGI',    nama_poli='Poli Gigi'),
        Poli(kode_poli='JANTUNG', nama_poli='Poli Jantung'),
        Poli(kode_poli='ANAK',    nama_poli='Poli Anak'),
        Poli(kode_poli='MATA',    nama_poli='Poli Mata'),
    ]
    db.session.add_all(poli_list)
    db.session.commit()
    print("✓ Data poli berhasil ditambahkan")

    # ── Data Dokter ────────────────────────
    dokter_list = [
        Dokter(nama_dokter='dr. Budi Santoso',    spesialisasi='Umum',     id_poli=1),
        Dokter(nama_dokter='dr. Siti Rahayu',     spesialisasi='Umum',     id_poli=1),
        Dokter(nama_dokter='drg. Ahmad Fauzi',    spesialisasi='Gigi',     id_poli=2),
        Dokter(nama_dokter='dr. Hendra Wijaya',   spesialisasi='Jantung',  id_poli=3),
        Dokter(nama_dokter='dr. Dewi Kusuma',     spesialisasi='Anak',     id_poli=4),
        Dokter(nama_dokter='dr. Retno Wulandari', spesialisasi='Mata',     id_poli=5),
    ]
    db.session.add_all(dokter_list)
    db.session.commit()
    print("✓ Data dokter berhasil ditambahkan")

    # ── Jadwal Dokter ──────────────────────
    jadwal_list = [
        JadwalDokter(id_dokter=1, hari='Senin',  jam_mulai=time(8,0),  jam_selesai=time(12,0)),
        JadwalDokter(id_dokter=1, hari='Rabu',   jam_mulai=time(8,0),  jam_selesai=time(12,0)),
        JadwalDokter(id_dokter=2, hari='Selasa', jam_mulai=time(13,0), jam_selesai=time(17,0)),
        JadwalDokter(id_dokter=2, hari='Kamis',  jam_mulai=time(13,0), jam_selesai=time(17,0)),
        JadwalDokter(id_dokter=3, hari='Senin',  jam_mulai=time(9,0),  jam_selesai=time(13,0)),
        JadwalDokter(id_dokter=4, hari='Selasa', jam_mulai=time(8,0),  jam_selesai=time(14,0)),
        JadwalDokter(id_dokter=5, hari='Rabu',   jam_mulai=time(8,0),  jam_selesai=time(12,0)),
        JadwalDokter(id_dokter=6, hari='Jumat',  jam_mulai=time(10,0), jam_selesai=time(15,0)),
    ]
    db.session.add_all(jadwal_list)
    db.session.commit()
    print("✓ Data jadwal dokter berhasil ditambahkan")

    print("\n✅ Seed selesai! Database siap digunakan.")
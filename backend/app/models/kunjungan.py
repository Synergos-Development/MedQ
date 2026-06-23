from app import db
from datetime import datetime

# ──────────────────────────────
# Model Kunjungan
# ──────────────────────────────
class Kunjungan(db.Model):
    __tablename__ = 'kunjungan'

    id_kunjungan  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_antrian    = db.Column(db.Integer, db.ForeignKey('antrian.id_antrian'), unique=True, nullable=False)
    id_pasien     = db.Column(db.Integer, db.ForeignKey('pasien.id_pasien'),   nullable=False)
    id_dokter     = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'),   nullable=False)
    waktu_masuk   = db.Column(db.DateTime, nullable=True)
    waktu_keluar  = db.Column(db.DateTime, nullable=True)
    keluhan       = db.Column(db.Text, nullable=True)
    diagnosa      = db.Column(db.Text, nullable=True)
    catatan_dokter = db.Column(db.Text, nullable=True)  # kolom tambahan dari ERD

    # Relasi ke resep (one-to-one, opsional)
    resep = db.relationship('Resep', backref='kunjungan', uselist=False, lazy=True, cascade='all, delete')

    def to_dict(self):
        return {
            'id_kunjungan':   self.id_kunjungan,
            'id_antrian':     self.id_antrian,
            'id_pasien':      self.id_pasien,
            'id_dokter':      self.id_dokter,
            'waktu_masuk':    str(self.waktu_masuk)  if self.waktu_masuk  else None,
            'waktu_keluar':   str(self.waktu_keluar) if self.waktu_keluar else None,
            'keluhan':        self.keluhan,
            'diagnosa':       self.diagnosa,
            'catatan_dokter': self.catatan_dokter,
        }

    def __repr__(self):
        return f'<Kunjungan {self.id_kunjungan} - Pasien {self.id_pasien}>'


# ──────────────────────────────
# Model Resep
# ──────────────────────────────
class Resep(db.Model):
    __tablename__ = 'resep'

    id_resep       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kunjungan   = db.Column(db.Integer, db.ForeignKey('kunjungan.id_kunjungan'), unique=True, nullable=False)
    tanggal_resep  = db.Column(db.DateTime, default=datetime.now)

    # Relasi ke detail resep
    detail = db.relationship('DetailResep', backref='resep', lazy=True, cascade='all, delete')

    def to_dict(self):
        return {
            'id_resep':      self.id_resep,
            'id_kunjungan':  self.id_kunjungan,
            'tanggal_resep': str(self.tanggal_resep),
            'detail':        [d.to_dict() for d in self.detail],
        }


# ──────────────────────────────
# Model Detail Resep
# ──────────────────────────────
class DetailResep(db.Model):
    __tablename__ = 'detail_resep'

    id_detail    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_resep     = db.Column(db.Integer, db.ForeignKey('resep.id_resep'), nullable=False)
    nama_obat    = db.Column(db.String(100), nullable=False)
    dosis        = db.Column(db.String(50),  nullable=True)
    aturan_pakai = db.Column(db.String(100), nullable=True)
    jumlah       = db.Column(db.Integer,     nullable=False)

    def to_dict(self):
        return {
            'id_detail':    self.id_detail,
            'id_resep':     self.id_resep,
            'nama_obat':    self.nama_obat,
            'dosis':        self.dosis,
            'aturan_pakai': self.aturan_pakai,
            'jumlah':       self.jumlah,
        }
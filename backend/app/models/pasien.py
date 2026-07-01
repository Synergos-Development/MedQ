from app import db
from datetime import datetime

class Pasien(db.Model):
    __tablename__ = 'pasien'

    id_pasien    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomor_rm     = db.Column(db.String(20), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    nik          = db.Column(db.String(20), unique=True, nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    alamat       = db.Column(db.Text, nullable=True)
    nomor_hp     = db.Column(db.String(20), nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.now)

    # Relasi ke tabel lain
    antrian      = db.relationship('Antrian',   backref='pasien', lazy=True)
    kunjungan    = db.relationship('Kunjungan', backref='pasien', lazy=True)

    def to_dict(self):
        """Konversi objek ke dictionary untuk response JSON"""
        return {
            'id_pasien':     self.id_pasien,
            'nomor_rm':      self.nomor_rm,
            'nama_lengkap':  self.nama_lengkap,
            'nik':           self.nik,
            'tanggal_lahir': str(self.tanggal_lahir),
            'alamat':        self.alamat,
            'nomor_hp':      self.nomor_hp,
            'created_at':    str(self.created_at),
        }

    def __repr__(self):
        return f'<Pasien {self.nomor_rm} - {self.nama_lengkap}>'
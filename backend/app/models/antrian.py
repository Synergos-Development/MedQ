from app import db
from datetime import datetime, date

class Antrian(db.Model):
    __tablename__ = 'antrian'

    # Status enum sesuai database kamu
    STATUS_MENUNGGU  = 'Menunggu'
    STATUS_DIPANGGIL = 'Dipanggil'
    STATUS_DIPERIKSA = 'Diperiksa'
    STATUS_SELESAI   = 'Selesai'
    STATUS_BATAL     = 'Batal'

    id_antrian      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomor_antrian   = db.Column(db.String(20), unique=True, nullable=False)
    id_pasien       = db.Column(db.Integer, db.ForeignKey('pasien.id_pasien'), nullable=False)
    id_poli         = db.Column(db.Integer, db.ForeignKey('poli.id_poli'),     nullable=False)
    id_dokter       = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'), nullable=False)
    tanggal         = db.Column(db.Date,     nullable=False, default=date.today)
    status          = db.Column(
                        db.Enum('Menunggu','Dipanggil','Diperiksa','Selesai','Batal'),
                        default='Menunggu'
                      )
    waktu_daftar    = db.Column(db.DateTime, default=datetime.now)
    waktu_dipanggil = db.Column(db.DateTime, nullable=True)

    # Relasi ke kunjungan (one-to-one)
    kunjungan = db.relationship('Kunjungan', backref='antrian', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id_antrian':      self.id_antrian,
            'nomor_antrian':   self.nomor_antrian,
            'id_pasien':       self.id_pasien,
            'id_poli':         self.id_poli,
            'id_dokter':       self.id_dokter,
            'tanggal':         str(self.tanggal),
            'status':          self.status,
            'waktu_daftar':    str(self.waktu_daftar),
            'waktu_dipanggil': str(self.waktu_dipanggil) if self.waktu_dipanggil else None,
        }

    def __repr__(self):
        return f'<Antrian {self.nomor_antrian} - {self.status}>'
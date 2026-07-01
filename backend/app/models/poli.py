from app import db

# ──────────────────────────────
# Model Poli
# ──────────────────────────────
class Poli(db.Model):
    __tablename__ = 'poli'

    id_poli    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kode_poli  = db.Column(db.String(10), unique=True, nullable=False)
    nama_poli  = db.Column(db.String(100), nullable=False)
    is_active  = db.Column(db.Boolean, default=True)

    # Relasi
    dokter  = db.relationship('Dokter',  backref='poli', lazy=True)
    antrian = db.relationship('Antrian', backref='poli', lazy=True)

    def to_dict(self):
        return {
            'id_poli':   self.id_poli,
            'kode_poli': self.kode_poli,
            'nama_poli': self.nama_poli,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return f'<Poli {self.kode_poli} - {self.nama_poli}>'


# ──────────────────────────────
# Model Dokter
# ──────────────────────────────
class Dokter(db.Model):
    __tablename__ = 'dokter'

    id_dokter    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_dokter  = db.Column(db.String(100), nullable=False)
    spesialisasi = db.Column(db.String(100), nullable=True)
    id_poli      = db.Column(db.Integer, db.ForeignKey('poli.id_poli'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    # Relasi
    jadwal    = db.relationship('JadwalDokter', backref='dokter', lazy=True, cascade='all, delete')
    antrian   = db.relationship('Antrian',      backref='dokter', lazy=True)
    kunjungan = db.relationship('Kunjungan',    backref='dokter', lazy=True)

    def to_dict(self):
        return {
            'id_dokter':    self.id_dokter,
            'nama_dokter':  self.nama_dokter,
            'spesialisasi': self.spesialisasi,
            'id_poli':      self.id_poli,
            'is_available': self.is_available,
        }

    def __repr__(self):
        return f'<Dokter {self.nama_dokter}>'


# ──────────────────────────────
# Model Jadwal Dokter
# ──────────────────────────────
class JadwalDokter(db.Model):
    __tablename__ = 'jadwal_dokter'

    HARI_CHOICES = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']

    id_jadwal   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dokter   = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'), nullable=False)
    hari        = db.Column(db.Enum('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu'), nullable=False)
    jam_mulai   = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)

    def to_dict(self):
        return {
            'id_jadwal':   self.id_jadwal,
            'id_dokter':   self.id_dokter,
            'hari':        self.hari,
            'jam_mulai':   str(self.jam_mulai),
            'jam_selesai': str(self.jam_selesai),
        }
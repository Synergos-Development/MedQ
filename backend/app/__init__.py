from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Inisialisasi ekstensi (belum terhubung ke app)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi ekstensi ke app
    db.init_app(app)
    CORS(app)  # izinkan frontend mengakses API

    # Daftarkan semua blueprint (routes)
    from app.routes.pasien import pasien_bp
    from app.routes.antrian import antrian_bp
    from app.routes.poli import poli_bp
    from app.routes.kunjungan import kunjungan_bp

    app.register_blueprint(pasien_bp,    url_prefix='/api/pasien')
    app.register_blueprint(antrian_bp,   url_prefix='/api/antrian')
    app.register_blueprint(poli_bp,      url_prefix='/api/poli')
    app.register_blueprint(kunjungan_bp, url_prefix='/api/kunjungan')
    
    from datetime import date
    from app.models.antrian import Antrian
    from app.algorithms.queue_poli import queue_manager
    
    with app.app_context():
        active_antrian = (
            Antrian.query
            .filter(
                Antrian.tanggal == date.today(),
                Antrian.status.in_([
                    'Menunggu',
                    'Dipanggil'
                ])
            )
            .order_by(
                Antrian.waktu_daftar.asc()
            )
            .all()
        )

        queue_manager.restore_queue(
            active_antrian
        )

    return app
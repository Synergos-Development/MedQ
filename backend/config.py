import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key untuk session Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-ganti-di-production'

    # Konfigurasi database MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/dbmedq'

    # Matikan notifikasi perubahan objek (hemat memori)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Tampilkan query SQL di terminal saat development
    SQLALCHEMY_ECHO = os.environ.get('FLASK_DEBUG') == 'True'
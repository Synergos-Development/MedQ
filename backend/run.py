from flask import Flask

# import blueprint route
from app.routes.pasien import pasien_bp
from app.routes.antrian import antrian_bp
from app.routes.kunjungan import kunjungan_bp
from app.routes.poli import poli_bp


def create_app():
# create_app()
# fungsi utama bikin aplikasi Flask

    # buat object Flask
    app = Flask(__name__)

    # daftar semua route
    app.register_blueprint(pasien_bp)
    app.register_blueprint(antrian_bp)
    app.register_blueprint(kunjungan_bp)
    app.register_blueprint(poli_bp)

    # register_blueprint()
    # supaya route di file lain dikenali Flask

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
    # # menjalankan server
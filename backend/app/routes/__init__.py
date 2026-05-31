from app.routes.antrian import antrian_bp
from app.routes.kunjungan import kunjungan_bp
from app.routes.pasien import pasien_bp
from app.routes.poli import poli_bp


def register_routes(app):

    app.register_blueprint(
        pasien_bp
    )

    app.register_blueprint(
        antrian_bp
    )

    app.register_blueprint(
        kunjungan_bp
    )

    app.register_blueprint(
        poli_bp
    )
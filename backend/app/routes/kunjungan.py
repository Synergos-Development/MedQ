from flask import Blueprint
from flask import jsonify

from app.services.kunjungan_service import (
    KunjunganService
)

kunjungan_bp = Blueprint(
    "kunjungan",
    __name__
)


@kunjungan_bp.route(
    "/api/kunjungan",
    methods=["GET"]
)
def semua():

    return jsonify(
        KunjunganService.all()
    )
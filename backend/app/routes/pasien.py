from flask import Blueprint
from flask import request
from flask import jsonify

from app.services.pendaftaran_service import (
    PendaftaranService
)

pasien_bp = Blueprint(
    "pasien",
    __name__
)


@pasien_bp.route(
    "/api/pasien",
    methods=["POST"]
)
def daftar_pasien():

    data = request.json

    pasien = PendaftaranService.create(
        data
    )

    return jsonify(pasien)


@pasien_bp.route(
    "/api/pasien/<rm>",
    methods=["GET"]
)
def get_pasien(rm):

    pasien = PendaftaranService.find(
        rm
    )

    return jsonify(pasien)
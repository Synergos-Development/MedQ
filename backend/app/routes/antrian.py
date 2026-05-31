from flask import Blueprint # kelompok endpoint
from flask import request # ambil data dari frontend
from flask import jsonify # ubah dict python jadi JSON

from app.services.antrian_service import AntreanService


# Blueprint = pengelompokan route
antrian_bp = Blueprint(
    "antrian",
    __name__
)


# ==========================
# ambil nomor antrean
# ==========================
@antrian_bp.route(
    "/api/antrian",
    methods=["POST"]
)
def ambil_antrian():

    data = request.json # ambil data dari frontend

    hasil = AntreanService.tambah_antrian(
        data["rm"],
        data["poli"]
    )

    return jsonify(hasil), 201
    # ubah dict python jadi JSON


# ==========================
# lihat antrean poli
# ==========================
@antrian_bp.route(
    "/api/antrian/<poli>",
    methods=["GET"]
)
def lihat_antrian(poli):

    hasil = AntreanService.get_queue(
        poli
    )

    return jsonify(hasil)


# ==========================
# panggil berikutnya
# ==========================
@antrian_bp.route(
    "/api/antrian/next/<poli>",
    methods=["POST"]
)
def panggil_berikutnya(poli):

    hasil = AntreanService.next_queue(
        poli
    )

    return jsonify(hasil)
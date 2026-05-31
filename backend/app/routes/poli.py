from flask import Blueprint
from flask import jsonify

poli_bp = Blueprint(
    "poli",
    __name__
)


@poli_bp.route(
    "/api/poli"
)
def get_poli():

    return jsonify([
        "umum",
        "gigi",
        "anak"
    ])
from flask import Blueprint, jsonify
from app.models.poli import Poli, Dokter

poli_bp = Blueprint('poli', __name__)

def ok(data=None, code=200):
    return jsonify({'status': 'success', 'data': data}), code

def err(message, code=400):
    return jsonify({'status': 'error', 'message': message}), code


# GET /api/poli/list
@poli_bp.route('/list', methods=['GET'])
def list_poli():
    poli_list = Poli.query.filter_by(is_active=True).all()
    return ok(data=[p.to_dict() for p in poli_list])


# GET /api/poli/<id_poli>/dokter
@poli_bp.route('/<int:id_poli>/dokter', methods=['GET'])
def dokter_poli(id_poli):
    poli = Poli.query.get(id_poli)
    if not poli:
        return err('Poli tidak ditemukan.', 404)

    dokter_list = Dokter.query.filter_by(id_poli=id_poli, is_available=True).all()
    return ok(data=[d.to_dict() for d in dokter_list])


# GET /api/poli/<id_poli>/antrian-aktif
@poli_bp.route('/<int:id_poli>/antrian-aktif', methods=['GET'])
def antrian_aktif(id_poli):
    from app.services.antrian_service import AntrianService
    hasil, error = AntrianService.get_antrian_aktif(id_poli)
    if error:
        return err(error)
    return ok(data=hasil)
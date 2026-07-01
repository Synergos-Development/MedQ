from flask import Blueprint, request, jsonify
from app.services.kunjungan_service import KunjunganService

kunjungan_bp = Blueprint('kunjungan', __name__)

def ok(data=None, message='success', code=200):
    return jsonify({'status': 'success', 'message': message, 'data': data}), code

def err(message, code=400):
    return jsonify({'status': 'error', 'message': message}), code


# POST /api/kunjungan/mulai
@kunjungan_bp.route('/mulai', methods=['POST'])
def mulai():
    data = request.get_json()
    if not data or not data.get('id_antrian'):
        return err('Field id_antrian wajib diisi.')

    hasil, error = KunjunganService.mulai_kunjungan(
        data['id_antrian'],
        data.get('keluhan', '')
    )
    if error:
        return err(error)

    return ok(data=hasil, message='Kunjungan dimulai.', code=201)


# POST /api/kunjungan/selesai
@kunjungan_bp.route('/selesai', methods=['POST'])
def selesai():
    data = request.get_json()
    if not data or not data.get('id_kunjungan'):
        return err('Field id_kunjungan wajib diisi.')

    hasil, error = KunjunganService.selesai_kunjungan(
        id_kunjungan   = data['id_kunjungan'],
        diagnosa       = data.get('diagnosa', ''),
        catatan_dokter = data.get('catatan_dokter', ''),
        resep_list     = data.get('resep', [])
    )
    if error:
        return err(error)

    return ok(data=hasil, message='Kunjungan selesai.')


# GET /api/kunjungan/<id_kunjungan>
@kunjungan_bp.route('/<int:id_kunjungan>', methods=['GET'])
def detail(id_kunjungan):
    hasil, error = KunjunganService.get_detail(id_kunjungan)
    if error:
        return err(error, 404)
    return ok(data=hasil)
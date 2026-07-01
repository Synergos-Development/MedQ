from flask import Blueprint, request, jsonify
from app.services.antrian_service import AntrianService

antrian_bp = Blueprint('antrian', __name__)

def ok(data=None, message='success', code=200):
    return jsonify({'status': 'success', 'message': message, 'data': data}), code

def err(message, code=400):
    return jsonify({'status': 'error', 'message': message}), code


# POST /api/antrian/ambil
@antrian_bp.route('/ambil', methods=['POST'])
def ambil():
    data = request.get_json()
    if not data:
        return err('Request body tidak boleh kosong.')

    required = ['id_pasien', 'id_poli', 'id_dokter']
    for field in required:
        if not data.get(field):
            return err(f'Field {field} wajib diisi.')

    hasil, error = AntrianService.ambil_nomor(
        data['id_pasien'],
        data['id_poli'],
        data['id_dokter']
    )
    if error:
        return err(error)

    return ok(data=hasil, message='Nomor antrian berhasil diambil.', code=201)


# GET /api/antrian/status/<nomor_antrian>
@antrian_bp.route('/status/<string:nomor_antrian>', methods=['GET'])
def status(nomor_antrian):
    hasil, error = AntrianService.cek_status(nomor_antrian)
    if error:
        return err(error, 404)
    return ok(data=hasil)


# POST /api/antrian/panggil
@antrian_bp.route('/panggil', methods=['POST'])
def panggil():
    data = request.get_json()
    if not data or not data.get('id_poli'):
        return err('Field id_poli wajib diisi.')

    hasil, error = AntrianService.panggil_berikutnya(
        data['id_poli'],
        data.get('id_dokter')
    )
    if error:
        return err(error, 404)

    return ok(data=hasil, message='Pasien berhasil dipanggil.')

# POST /api/antrian/diperiksa
@antrian_bp.route('/diperiksa', methods=['POST'])
def diperiksa():
    data = request.get_json()

    if not data or not data.get('id_antrian'):
        return err('Field id_antrian wajib diisi.')

    hasil, error = AntrianService.mulai_periksa(
        data['id_antrian']
    )

    if error:
        return err(error)

    return ok(
        data=hasil,
        message='Pasien mulai diperiksa.'
    )
    
# POST /api/antrian/selesai
@antrian_bp.route('/selesai', methods=['POST'])
def selesai():
    data = request.get_json()

    if not data or not data.get('id_antrian'):
        return err('Field id_antrian wajib diisi.')

    hasil, error = AntrianService.selesaikan(
        data['id_antrian']
    )

    if error:
        return err(error)

    return ok(
        data=hasil,
        message='Pemeriksaan selesai.'
    )

# POST /api/antrian/batal
@antrian_bp.route('/batal', methods=['POST'])
def batal():
    data = request.get_json()
    if not data or not data.get('id_antrian'):
        return err('Field id_antrian wajib diisi.')

    pesan, error = AntrianService.batalkan(data['id_antrian'])
    if error:
        return err(error)

    return ok(message=pesan)


# GET /api/antrian/aktif/<id_poli>  — untuk layar display
@antrian_bp.route('/aktif/<int:id_poli>', methods=['GET'])
def aktif(id_poli):
    hasil, error = AntrianService.get_antrian_aktif(id_poli)
    if error:
        return err(error)
    return ok(data=hasil)
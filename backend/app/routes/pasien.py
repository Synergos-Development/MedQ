from flask import Blueprint, request, jsonify
from app.services.pendaftaran_service import PendaftaranService

pasien_bp = Blueprint('pasien', __name__)

# ── Helper response ──────────────────────────────
def ok(data=None, message='success', code=200):
    return jsonify({'status': 'success', 'message': message, 'data': data}), code

def err(message, code=400):
    return jsonify({'status': 'error', 'message': message}), code


# POST /api/pasien/daftar
@pasien_bp.route('/daftar', methods=['POST'])
def daftar():
    data = request.get_json()
    if not data:
        return err('Request body tidak boleh kosong.')

    # Validasi field wajib
    required = ['nama_lengkap', 'nik', 'tanggal_lahir']
    for field in required:
        if not data.get(field):
            return err(f'Field {field} wajib diisi.')

    pasien, error = PendaftaranService.daftar_pasien_baru(data)
    if error:
        return err(error)

    return ok(
        data    = pasien.to_dict(),
        message = 'Pasien berhasil didaftarkan.',
        code    = 201
    )


# POST /api/pasien/verifikasi
@pasien_bp.route('/verifikasi', methods=['POST'])
def verifikasi():
    data = request.get_json()
    if not data or not data.get('nomor_rm'):
        return err('Nomor RM wajib diisi.')

    pasien, error = PendaftaranService.verifikasi_pasien(data['nomor_rm'])
    if error:
        return err(error, 404)

    return ok(data=pasien.to_dict())


# GET /api/pasien/cari?nama=budi
@pasien_bp.route('/cari', methods=['GET'])
def cari():
    nama = request.args.get('nama', '').strip()
    if not nama:
        return err('Parameter nama wajib diisi.')

    hasil = PendaftaranService.cari_pasien(nama)
    return ok(data=[p.to_dict() for p in hasil])


# GET /api/pasien/<id_pasien>/riwayat
@pasien_bp.route('/<int:id_pasien>/riwayat', methods=['GET'])
def riwayat(id_pasien):
    hasil = PendaftaranService.get_riwayat(id_pasien)
    return ok(data=hasil)
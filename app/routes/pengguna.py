from flask import Blueprint, request
from app.extensions import db
from app.models import Pengguna
from app.utils.responses import api_response, error_response

pengguna_bp = Blueprint('pengguna', __name__, url_prefix='/pengguna')

# GET /pengguna - Ambil daftar pengguna
@pengguna_bp.route('', methods=['GET'])
def get_all_pengguna():
    try:
        peran = request.args.get('peran')
        if peran:
            pengguna_list = Pengguna.query.filter_by(peran=peran).all()
        else:
            pengguna_list = Pengguna.query.all()

        return api_response(
            status="success",
            message="Data pengguna berhasil diambil",
            data=[item.to_dict() for item in pengguna_list],
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil pengguna: {str(e)}", status_code=500)


# GET /pengguna/<id> - Detail pengguna
@pengguna_bp.route('/<int:id_pengguna>', methods=['GET'])
def get_pengguna_by_id(id_pengguna):
    try:
        user = Pengguna.query.get(id_pengguna)
        if not user:
            return error_response(message=f"Pengguna ID {id_pengguna} tidak ditemukan", status_code=404)

        return api_response(
            status="success",
            message="Detail pengguna ditemukan",
            data=user.to_dict(),
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil detail pengguna: {str(e)}", status_code=500)


# POST /pengguna - Tambah pengguna baru
@pengguna_bp.route('', methods=['POST'])
def create_pengguna():
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    for field in ['nama', 'email', 'peran']:
        if not data.get(field):
            return error_response(message=f"Field '{field}' wajib diisi", status_code=400)

    peran_valid = ['donatur', 'penerima', 'relawan', 'admin']
    if data['peran'] not in peran_valid:
        return error_response(message=f"Peran tidak valid. Pilihan: {', '.join(peran_valid)}", status_code=400)

    # Cek duplikasi email
    existing_user = Pengguna.query.filter_by(email=data['email']).first()
    if existing_user:
        return error_response(message="Email sudah terdaftar", status_code=400)

    try:
        new_user = Pengguna(
            nama=data['nama'],
            email=data['email'],
            nomor_hp=data.get('nomor_hp'),
            alamat=data.get('alamat'),
            peran=data['peran']
        )
        db.session.add(new_user)
        db.session.commit()

        return api_response(
            status="success",
            message="Pengguna berhasil didaftarkan",
            data=new_user.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal mendaftarkan pengguna: {str(e)}", status_code=500)


# PUT /pengguna/<id> - Edit data pengguna
@pengguna_bp.route('/<int:id_pengguna>', methods=['PUT', 'PATCH'])
def update_pengguna(id_pengguna):
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    user = Pengguna.query.get(id_pengguna)
    if not user:
        return error_response(message=f"Pengguna ID {id_pengguna} tidak ditemukan", status_code=404)

    try:
        if 'nama' in data:
            user.nama = data['nama']
        if 'nomor_hp' in data:
            user.nomor_hp = data['nomor_hp']
        if 'alamat' in data:
            user.alamat = data['alamat']
        if 'peran' in data:
            peran_valid = ['donatur', 'penerima', 'relawan', 'admin']
            if data['peran'] not in peran_valid:
                return error_response(message=f"Peran tidak valid. Pilihan: {', '.join(peran_valid)}", status_code=400)
            user.peran = data['peran']

        db.session.commit()
        return api_response(
            status="success",
            message="Data pengguna berhasil diperbarui",
            data=user.to_dict(),
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal memperbarui pengguna: {str(e)}", status_code=500)


# DELETE /pengguna/<id> - Hapus data pengguna
@pengguna_bp.route('/<int:id_pengguna>', methods=['DELETE'])
def delete_pengguna(id_pengguna):
    user = Pengguna.query.get(id_pengguna)
    if not user:
        return error_response(message=f"Pengguna ID {id_pengguna} tidak ditemukan", status_code=404)

    try:
        db.session.delete(user)
        db.session.commit()
        return api_response(
            status="success",
            message=f"Pengguna ID {id_pengguna} berhasil dihapus",
            data=None,
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal menghapus pengguna: {str(e)}", status_code=500)

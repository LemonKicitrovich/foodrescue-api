from flask import Blueprint, request
from datetime import datetime
from app.extensions import db
from app.models import Donasi, Pengguna
from app.utils.responses import api_response, error_response

donasi_bp = Blueprint('donasi', __name__, url_prefix='/donasi')

# 1. GET /donasi - Mendapatkan semua daftar donasi makanan
@donasi_bp.route('', methods=['GET'])
def get_all_donasi():
    try:
        # Opsional filter berdasarkan status (contoh: /donasi?status=tersedia)
        status = request.args.get('status')
        if status:
            daftar_donasi = Donasi.query.filter_by(status=status).all()
        else:
            daftar_donasi = Donasi.query.all()
            
        return api_response(
            status="success",
            message="Data donasi berhasil diambil",
            data=[item.to_dict() for item in daftar_donasi],
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil data donasi: {str(e)}", status_code=500)


# 2. GET /donasi/<id> - Mendapatkan detail satu donasi berdasarkan ID
@donasi_bp.route('/<int:id_donasi>', methods=['GET'])
def get_donasi_by_id(id_donasi):
    try:
        donasi = Donasi.query.get(id_donasi)
        if not donasi:
            return error_response(message=f"Donasi dengan ID {id_donasi} tidak ditemukan", status_code=404)

        return api_response(
            status="success",
            message="Detail donasi ditemukan",
            data=donasi.to_dict(),
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil detail donasi: {str(e)}", status_code=500)


# 3. POST /donasi - Menambahkan donasi makanan baru
@donasi_bp.route('', methods=['POST'])
def create_donasi():
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    # Validasi field wajib
    required_fields = ['id_donatur', 'nama_makanan', 'jumlah', 'lokasi_pengambilan', 'tanggal_kadaluarsa']
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            return error_response(message=f"Field '{field}' wajib diisi", status_code=400)

    # Validasi id_donatur ada di tabel pengguna
    donatur = Pengguna.query.get(data['id_donatur'])
    if not donatur:
        return error_response(message="Donatur tidak ditemukan", status_code=404)
        
    if donatur.peran != 'donatur':
        return error_response(message="Pengguna yang dipilih bukan donatur", status_code=400)

    # Validasi jumlah
    if int(data['jumlah']) <= 0:
        return error_response(message="Jumlah makanan harus lebih dari 0", status_code=400)

    # Parsing tanggal
    try:
        tgl_kadaluarsa = datetime.strptime(data['tanggal_kadaluarsa'], '%Y-%m-%d').date()
    except ValueError:
        return error_response(message="Format tanggal_kadaluarsa tidak valid (gunakan YYYY-MM-DD)", status_code=400)

    try:
        new_donasi = Donasi(
            id_donatur=data['id_donatur'],
            nama_makanan=data['nama_makanan'],
            jumlah=data['jumlah'],
            lokasi_pengambilan=data['lokasi_pengambilan'],
            tanggal_kadaluarsa=tgl_kadaluarsa,
            status=data.get('status', 'tersedia')
        )
        db.session.add(new_donasi)
        db.session.commit()

        return api_response(
            status="success",
            message="Donasi makanan berhasil didaftarkan",
            data=new_donasi.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal menambahkan donasi: {str(e)}", status_code=500)


# 4. PUT /donasi/<id> - Mengubah data donasi atau statusnya
@donasi_bp.route('/<int:id_donasi>', methods=['PUT', 'PATCH'])
def update_donasi(id_donasi):
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    donasi = Donasi.query.get(id_donasi)
    if not donasi:
        return error_response(message=f"Donasi dengan ID {id_donasi} tidak ditemukan", status_code=404)

    try:
        if 'nama_makanan' in data:
            donasi.nama_makanan = data['nama_makanan']
        if 'jumlah' in data:
            if int(data['jumlah']) <= 0:
                return error_response(message="Jumlah makanan harus lebih dari 0", status_code=400)
            donasi.jumlah = data['jumlah']
        if 'lokasi_pengambilan' in data:
            donasi.lokasi_pengambilan = data['lokasi_pengambilan']
        if 'tanggal_kadaluarsa' in data:
            try:
                donasi.tanggal_kadaluarsa = datetime.strptime(data['tanggal_kadaluarsa'], '%Y-%m-%d').date()
            except ValueError:
                return error_response(message="Format tanggal_kadaluarsa tidak valid (gunakan YYYY-MM-DD)", status_code=400)
        if 'status' in data:
            status_valid = ['tersedia', 'dipesan', 'selesai', 'dibatalkan']
            if data['status'] not in status_valid:
                return error_response(message=f"Status tidak valid. Pilihan: {', '.join(status_valid)}", status_code=400)
            donasi.status = data['status']

        db.session.commit()

        return api_response(
            status="success",
            message="Data donasi berhasil diperbarui",
            data=donasi.to_dict(),
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal memperbarui donasi: {str(e)}", status_code=500)


# 5. DELETE /donasi/<id> - Menghapus data donasi
@donasi_bp.route('/<int:id_donasi>', methods=['DELETE'])
def delete_donasi(id_donasi):
    donasi = Donasi.query.get(id_donasi)
    if not donasi:
        return error_response(message=f"Donasi dengan ID {id_donasi} tidak ditemukan", status_code=404)

    try:
        db.session.delete(donasi)
        db.session.commit()

        return api_response(
            status="success",
            message=f"Donasi dengan ID {id_donasi} berhasil dihapus",
            data=None,
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal menghapus donasi: {str(e)}", status_code=500)

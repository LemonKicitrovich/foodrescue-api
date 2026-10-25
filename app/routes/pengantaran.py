from flask import Blueprint, request
from datetime import date
from app.extensions import db
from app.models import Pengantaran, Donasi, Pengguna
from app.utils.responses import api_response, error_response

pengantaran_bp = Blueprint('pengantaran', __name__, url_prefix='/pengantaran')

# GET /pengantaran - Daftar pengantaran donasi
@pengantaran_bp.route('', methods=['GET'])
def get_all_pengantaran():
    try:
        daftar = Pengantaran.query.all()
        return api_response(
            status="success",
            message="Data pengantaran berhasil diambil",
            data=[item.to_dict() for item in daftar],
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil data pengantaran: {str(e)}", status_code=500)


# POST /pengantaran - Membuat permintaan pengantaran donasi ke penerima
@pengantaran_bp.route('', methods=['POST'])
def create_pengantaran():
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    for field in ['id_donasi', 'id_penerima']:
        if not data.get(field):
            return error_response(message=f"Field '{field}' wajib diisi", status_code=400)

    # Validasi donasi
    donasi = Donasi.query.get(data['id_donasi'])
    if not donasi:
        return error_response(message="Donasi tidak ditemukan", status_code=404)

    if donasi.status != 'tersedia':
        return error_response(message="Donasi tidak dalam status tersedia", status_code=400)

    # Validasi penerima
    penerima = Pengguna.query.get(data['id_penerima'])
    if not penerima or penerima.peran != 'penerima':
        return error_response(message="Penerima tidak valid (harus terdaftar dengan peran 'penerima')", status_code=400)

    # Validasi relawan jika disertakan
    id_relawan = data.get('id_relawan')
    if id_relawan:
        relawan = Pengguna.query.get(id_relawan)
        if not relawan or relawan.peran != 'relawan':
            return error_response(message="Relawan tidak valid (harus terdaftar dengan peran 'relawan')", status_code=400)

    try:
        # Buat order pengantaran baru
        pengantaran_baru = Pengantaran(
            id_donasi=data['id_donasi'],
            id_penerima=data['id_penerima'],
            id_relawan=id_relawan,
            status_pengantaran='menunggu',
            tanggal_pengantaran=date.today()
        )
        # Update status donasi menjadi 'dipesan'
        donasi.status = 'dipesan'

        db.session.add(pengantaran_baru)
        db.session.commit()

        return api_response(
            status="success",
            message="Pesanan pengantaran donasi berhasil dibuat",
            data=pengantaran_baru.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal membuat pengantaran: {str(e)}", status_code=500)


# PUT /pengantaran/<id> - Update status pengantaran (misal dari menunggu -> diambil -> diantar -> selesai)
@pengantaran_bp.route('/<int:id_pengantaran>', methods=['PUT', 'PATCH'])
def update_status_pengantaran(id_pengantaran):
    data = request.get_json()
    if not data or 'status_pengantaran' not in data:
        return error_response(message="Field 'status_pengantaran' wajib diisi", status_code=400)

    status_valid = ['menunggu', 'diambil', 'diantar', 'selesai']
    if data['status_pengantaran'] not in status_valid:
        return error_response(message=f"Status tidak valid. Pilihan: {', '.join(status_valid)}", status_code=400)

    pengantaran = Pengantaran.query.get(id_pengantaran)
    if not pengantaran:
        return error_response(message=f"Pengantaran ID {id_pengantaran} tidak ditemukan", status_code=404)

    try:
        pengantaran.status_pengantaran = data['status_pengantaran']
        if 'id_relawan' in data:
            pengantaran.id_relawan = data['id_relawan']

        # Jika selesai, update status donasi menjadi 'selesai'
        if data['status_pengantaran'] == 'selesai':
            donasi = Donasi.query.get(pengantaran.id_donasi)
            if donasi:
                donasi.status = 'selesai'

        db.session.commit()

        return api_response(
            status="success",
            message="Status pengantaran berhasil diperbarui",
            data=pengantaran.to_dict(),
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal memperbarui status pengantaran: {str(e)}", status_code=500)

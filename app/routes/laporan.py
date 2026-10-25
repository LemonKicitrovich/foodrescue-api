from flask import Blueprint, request
from app.extensions import db
from app.models import LaporanMasalah, Donasi, Pengguna
from app.utils.responses import api_response, error_response

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')

# GET /laporan - Daftar semua laporan masalah
@laporan_bp.route('', methods=['GET'])
def get_all_laporan():
    try:
        daftar = LaporanMasalah.query.all()
        return api_response(
            status="success",
            message="Data laporan masalah berhasil diambil",
            data=[item.to_dict() for item in daftar],
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil laporan masalah: {str(e)}", status_code=500)


# POST /laporan - Membuat laporan masalah baru
@laporan_bp.route('', methods=['POST'])
def create_laporan():
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    for field in ['id_donasi', 'id_pelapor', 'isi_laporan']:
        if not data.get(field):
            return error_response(message=f"Field '{field}' wajib diisi", status_code=400)

    donasi = Donasi.query.get(data['id_donasi'])
    if not donasi:
        return error_response(message="Donasi tidak ditemukan", status_code=404)

    pelapor = Pengguna.query.get(data['id_pelapor'])
    if not pelapor:
        return error_response(message="Pengguna pelapor tidak ditemukan", status_code=404)

    try:
        laporan_baru = LaporanMasalah(
            id_donasi=data['id_donasi'],
            id_pelapor=data['id_pelapor'],
            isi_laporan=data['isi_laporan'],
            status_laporan=data.get('status_laporan', 'belum ditangani')
        )
        db.session.add(laporan_baru)
        db.session.commit()

        return api_response(
            status="success",
            message="Laporan masalah berhasil dikirim",
            data=laporan_baru.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal membuat laporan: {str(e)}", status_code=500)


# PUT /laporan/<id> - Mengubah status penanganan laporan (admin)
@laporan_bp.route('/<int:id_laporan>', methods=['PUT', 'PATCH'])
def update_status_laporan(id_laporan):
    data = request.get_json()
    if not data or 'status_laporan' not in data:
        return error_response(message="Field 'status_laporan' wajib diisi", status_code=400)

    status_valid = ['belum ditangani', 'diproses', 'selesai']
    if data['status_laporan'] not in status_valid:
        return error_response(message=f"Status tidak valid. Pilihan: {', '.join(status_valid)}", status_code=400)

    laporan = LaporanMasalah.query.get(id_laporan)
    if not laporan:
        return error_response(message=f"Laporan ID {id_laporan} tidak ditemukan", status_code=404)

    try:
        laporan.status_laporan = data['status_laporan']
        db.session.commit()

        return api_response(
            status="success",
            message="Status laporan berhasil diperbarui",
            data=laporan.to_dict(),
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal memperbarui status laporan: {str(e)}", status_code=500)

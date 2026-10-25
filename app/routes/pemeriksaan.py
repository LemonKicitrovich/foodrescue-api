from flask import Blueprint, request
from app.extensions import db
from app.models import PemeriksaanMakanan, Donasi, Pengguna
from app.utils.responses import api_response, error_response

pemeriksaan_bp = Blueprint('pemeriksaan', __name__, url_prefix='/pemeriksaan')

# GET /pemeriksaan - Melihat hasil pemeriksaan kualitas makanan
@pemeriksaan_bp.route('', methods=['GET'])
def get_all_pemeriksaan():
    try:
        daftar = PemeriksaanMakanan.query.all()
        return api_response(
            status="success",
            message="Data pemeriksaan makanan berhasil diambil",
            data=[item.to_dict() for item in daftar],
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Gagal mengambil data pemeriksaan: {str(e)}", status_code=500)


# POST /pemeriksaan - Input hasil quality check makanan oleh relawan/admin
@pemeriksaan_bp.route('', methods=['POST'])
def create_pemeriksaan():
    data = request.get_json()
    if not data:
        return error_response(message="Body request wajib berupa JSON", status_code=400)

    for field in ['id_donasi', 'id_pemeriksa', 'kondisi']:
        if field not in data or data[field] is None:
            return error_response(message=f"Field '{field}' wajib diisi", status_code=400)

    # Validasi kondisi
    if data['kondisi'] not in ['layak', 'tidak layak']:
        return error_response(message="Kondisi harus 'layak' atau 'tidak layak'", status_code=400)

    # Validasi donasi
    donasi = Donasi.query.get(data['id_donasi'])
    if not donasi:
        return error_response(message="Donasi tidak ditemukan", status_code=404)

    # Cek apakah donasi sudah pernah diperiksa
    existing = PemeriksaanMakanan.query.filter_by(id_donasi=data['id_donasi']).first()
    if existing:
        return error_response(message="Donasi ini sudah pernah diperiksa", status_code=400)

    # Validasi pemeriksa (relawan atau admin)
    pemeriksa = Pengguna.query.get(data['id_pemeriksa'])
    if not pemeriksa or pemeriksa.peran not in ['relawan', 'admin']:
        return error_response(message="Pemeriksa harus berstatus relawan atau admin", status_code=400)

    try:
        new_periksa = PemeriksaanMakanan(
            id_donasi=data['id_donasi'],
            id_pemeriksa=data['id_pemeriksa'],
            kondisi=data['kondisi'],
            catatan=data.get('catatan', '')
        )
        db.session.add(new_periksa)

        # Jika tidak layak, update status donasi menjadi 'dibatalkan'
        if data['kondisi'] == 'tidak layak':
            donasi.status = 'dibatalkan'

        db.session.commit()

        return api_response(
            status="success",
            message="Pemeriksaan makanan berhasil disimpan",
            data=new_periksa.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Gagal menyimpan pemeriksaan: {str(e)}", status_code=500)

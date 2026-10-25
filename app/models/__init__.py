from app.extensions import db
from datetime import date

class Pengguna(db.Model):
    __tablename__ = 'pengguna'

    id_pengguna = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nomor_hp = db.Column(db.String(20), nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    peran = db.Column(db.String(20), nullable=False)  # 'donatur', 'penerima', 'relawan', 'admin'

    # Relasi
    donasi_list = db.relationship('Donasi', backref='donatur', cascade='all, delete-orphan', lazy=True)
    pemeriksaan_list = db.relationship('PemeriksaanMakanan', backref='pemeriksa', lazy=True)

    def to_dict(self):
        return {
            'id_pengguna': self.id_pengguna,
            'nama': self.nama,
            'email': self.email,
            'nomor_hp': self.nomor_hp,
            'alamat': self.alamat,
            'peran': self.peran
        }


class Donasi(db.Model):
    __tablename__ = 'donasi'

    id_donasi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_donatur = db.Column(db.Integer, db.ForeignKey('pengguna.id_pengguna', ondelete='CASCADE'), nullable=False)
    nama_makanan = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    lokasi_pengambilan = db.Column(db.Text, nullable=False)
    tanggal_kadaluarsa = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='tersedia')  # 'tersedia', 'dipesan', 'selesai', 'dibatalkan'

    # Relasi
    pemeriksaan = db.relationship('PemeriksaanMakanan', backref='donasi', uselist=False, cascade='all, delete-orphan', lazy=True)
    pengantaran_list = db.relationship('Pengantaran', backref='donasi', cascade='all, delete-orphan', lazy=True)
    laporan_list = db.relationship('LaporanMasalah', backref='donasi', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id_donasi': self.id_donasi,
            'id_donatur': self.id_donatur,
            'nama_donatur': self.donatur.nama if self.donatur else None,
            'nama_makanan': self.nama_makanan,
            'jumlah': self.jumlah,
            'lokasi_pengambilan': self.lokasi_pengambilan,
            'tanggal_kadaluarsa': self.tanggal_kadaluarsa.isoformat() if self.tanggal_kadaluarsa else None,
            'status': self.status
        }


class PemeriksaanMakanan(db.Model):
    __tablename__ = 'pemeriksaan_makanan'

    id_pemeriksaan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_donasi = db.Column(db.Integer, db.ForeignKey('donasi.id_donasi', ondelete='CASCADE'), nullable=False, unique=True)
    id_pemeriksa = db.Column(db.Integer, db.ForeignKey('pengguna.id_pengguna', ondelete='CASCADE'), nullable=False)
    kondisi = db.Column(db.String(20), nullable=False)  # 'layak', 'tidak layak'
    catatan = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id_pemeriksaan': self.id_pemeriksaan,
            'id_donasi': self.id_donasi,
            'nama_makanan': self.donasi.nama_makanan if self.donasi else None,
            'id_pemeriksa': self.id_pemeriksa,
            'nama_pemeriksa': self.pemeriksa.nama if self.pemeriksa else None,
            'kondisi': self.kondisi,
            'catatan': self.catatan
        }


class Pengantaran(db.Model):
    __tablename__ = 'pengantaran'

    id_pengantaran = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_donasi = db.Column(db.Integer, db.ForeignKey('donasi.id_donasi', ondelete='CASCADE'), nullable=False)
    id_penerima = db.Column(db.Integer, db.ForeignKey('pengguna.id_pengguna', ondelete='CASCADE'), nullable=False)
    id_relawan = db.Column(db.Integer, db.ForeignKey('pengguna.id_pengguna', ondelete='SET NULL'), nullable=True)
    status_pengantaran = db.Column(db.String(20), nullable=False, default='menunggu')  # 'menunggu', 'diambil', 'diantar', 'selesai'
    tanggal_pengantaran = db.Column(db.Date, nullable=True)

    # Relasi khusus ke pengguna penerima dan relawan
    penerima = db.relationship('Pengguna', foreign_keys=[id_penerima], backref='pengantaran_terima')
    relawan = db.relationship('Pengguna', foreign_keys=[id_relawan], backref='pengantaran_antar')

    def to_dict(self):
        return {
            'id_pengantaran': self.id_pengantaran,
            'id_donasi': self.id_donasi,
            'nama_makanan': self.donasi.nama_makanan if self.donasi else None,
            'id_penerima': self.id_penerima,
            'nama_penerima': self.penerima.nama if self.penerima else None,
            'id_relawan': self.id_relawan,
            'nama_relawan': self.relawan.nama if self.relawan else None,
            'status_pengantaran': self.status_pengantaran,
            'tanggal_pengantaran': self.tanggal_pengantaran.isoformat() if self.tanggal_pengantaran else None
        }


class LaporanMasalah(db.Model):
    __tablename__ = 'laporan_masalah'

    id_laporan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_donasi = db.Column(db.Integer, db.ForeignKey('donasi.id_donasi', ondelete='CASCADE'), nullable=False)
    id_pelapor = db.Column(db.Integer, db.ForeignKey('pengguna.id_pengguna', ondelete='CASCADE'), nullable=False)
    isi_laporan = db.Column(db.Text, nullable=False)
    status_laporan = db.Column(db.String(20), nullable=False, default='belum ditangani')  # 'belum ditangani', 'diproses', 'selesai'

    pelapor = db.relationship('Pengguna', foreign_keys=[id_pelapor], backref='laporan_list')

    def to_dict(self):
        return {
            'id_laporan': self.id_laporan,
            'id_donasi': self.id_donasi,
            'id_pelapor': self.id_pelapor,
            'nama_pelapor': self.pelapor.nama if self.pelapor else None,
            'isi_laporan': self.isi_laporan,
            'status_laporan': self.status_laporan
        }

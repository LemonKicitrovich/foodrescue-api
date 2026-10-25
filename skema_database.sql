-- ========================================================
-- Tugas Akhir Learning Labs: Backend Development
-- Nama  : Raihan Noviansyah
-- NIM   : 21114012610124
-- Judul : FoodRescue API
-- ========================================================

DROP TABLE IF EXISTS laporan_masalah CASCADE;
DROP TABLE IF EXISTS pengantaran CASCADE;
DROP TABLE IF EXISTS pemeriksaan_makanan CASCADE;
DROP TABLE IF EXISTS donasi CASCADE;
DROP TABLE IF EXISTS pengguna CASCADE;

-- 1. Menyimpan data semua pengguna aplikasi
CREATE TABLE pengguna (
    id_pengguna SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nomor_hp VARCHAR(20),
    alamat TEXT,
    peran VARCHAR(20) NOT NULL
        CHECK (peran IN ('donatur', 'penerima', 'relawan', 'admin'))
);

-- 2. Menyimpan makanan yang diberikan oleh donatur
CREATE TABLE donasi (
    id_donasi SERIAL PRIMARY KEY,
    id_donatur INTEGER NOT NULL,
    nama_makanan VARCHAR(100) NOT NULL,
    jumlah INTEGER NOT NULL CHECK (jumlah > 0),
    lokasi_pengambilan TEXT NOT NULL,
    tanggal_kadaluarsa DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'tersedia'
        CHECK (status IN ('tersedia', 'dipesan', 'selesai', 'dibatalkan')),

    FOREIGN KEY (id_donatur)
        REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
);

-- 3. Menyimpan hasil pemeriksaan kondisi makanan
CREATE TABLE pemeriksaan_makanan (
    id_pemeriksaan SERIAL PRIMARY KEY,
    id_donasi INTEGER NOT NULL UNIQUE,
    id_pemeriksa INTEGER NOT NULL,
    kondisi VARCHAR(20) NOT NULL
        CHECK (kondisi IN ('layak', 'tidak layak')),
    catatan TEXT,

    FOREIGN KEY (id_donasi)
        REFERENCES donasi(id_donasi) ON DELETE CASCADE,
    FOREIGN KEY (id_pemeriksa)
        REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
);

-- 4. Menyimpan proses pengantaran makanan ke penerima
CREATE TABLE pengantaran (
    id_pengantaran SERIAL PRIMARY KEY,
    id_donasi INTEGER NOT NULL,
    id_penerima INTEGER NOT NULL,
    id_relawan INTEGER,
    status_pengantaran VARCHAR(20) NOT NULL DEFAULT 'menunggu'
        CHECK (status_pengantaran IN ('menunggu', 'diambil', 'diantar', 'selesai')),
    tanggal_pengantaran DATE,

    FOREIGN KEY (id_donasi)
        REFERENCES donasi(id_donasi) ON DELETE CASCADE,
    FOREIGN KEY (id_penerima)
        REFERENCES pengguna(id_pengguna) ON DELETE CASCADE,
    FOREIGN KEY (id_relawan)
        REFERENCES pengguna(id_pengguna) ON DELETE SET NULL
);

-- 5. Menyimpan laporan jika terjadi masalah
CREATE TABLE laporan_masalah (
    id_laporan SERIAL PRIMARY KEY,
    id_donasi INTEGER NOT NULL,
    id_pelapor INTEGER NOT NULL,
    isi_laporan TEXT NOT NULL,
    status_laporan VARCHAR(20) NOT NULL DEFAULT 'belum ditangani'
        CHECK (status_laporan IN ('belum ditangani', 'diproses', 'selesai')),

    FOREIGN KEY (id_donasi)
        REFERENCES donasi(id_donasi) ON DELETE CASCADE,
    FOREIGN KEY (id_pelapor)
        REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
);

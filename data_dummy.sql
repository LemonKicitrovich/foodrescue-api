-- ========================================================
-- Data Dummy untuk Pengujian FoodRescue API
-- ========================================================

-- 1. Insert Pengguna
INSERT INTO pengguna (nama, email, nomor_hp, alamat, peran) VALUES
('Restoran Padang Minang Saiyo', 'admin@minangsaiyo.com', '081234567890', 'Jl. Merdeka No. 45, Jakarta Pusat', 'donatur'),
('Bakery Roti Manis', 'kontak@rotimanis.com', '082198765432', 'Jl. Sudirman No. 12, Jakarta Selatan', 'donatur'),
('Panti Asuhan Kasih Bunda', 'pengurus@kasihbunda.org', '085711223344', 'Jl. Kenanga No. 8, Jakarta Timur', 'penerima'),
('Komunitas Lansia Sejahtera', 'lansia@sejahtera.org', '081399887766', 'Jl. Mawar No. 19, Depok', 'penerima'),
('Budi Santoso', 'budi.santoso@gmail.com', '081288776655', 'Jl. Tebet Barat No. 3, Jakarta Selatan', 'relawan'),
('Siti Rahmawati', 'siti.rahmawati@gmail.com', '081277665544', 'Jl. Margonda No. 100, Depok', 'relawan'),
('Raihan Noviansyah (Admin)', 'raihan.noviansyah@foodrescue.id', '081122334455', 'Jakarta', 'admin');

-- 2. Insert Donasi
INSERT INTO donasi (id_donatur, nama_makanan, jumlah, lokasi_pengambilan, tanggal_kadaluarsa, status) VALUES
(1, 'Nasi Kotak Rendang & Ayam Gulai', 25, 'Restoran Padang Minang Saiyo, Jl. Merdeka 45', CURRENT_DATE + INTERVAL '1 day', 'tersedia'),
(2, 'Roti Gandum dan Croissant Aneka Rasa', 40, 'Bakery Roti Manis, Jl. Sudirman 12', CURRENT_DATE + INTERVAL '2 day', 'tersedia'),
(1, 'Lauk Ikan Bakar & Sayur Nangka', 15, 'Restoran Padang Minang Saiyo, Jl. Merdeka 45', CURRENT_DATE + INTERVAL '1 day', 'dipesan');

-- 3. Insert Pemeriksaan Makanan
INSERT INTO pemeriksaan_makanan (id_donasi, id_pemeriksa, kondisi, catatan) VALUES
(1, 5, 'layak', 'Kemasan higienis, porsi baru dimasak sore hari dan masih hangat.'),
(2, 6, 'layak', 'Roti kemasan rapi dan segel utuh, aroma segar.');

-- 4. Insert Pengantaran
INSERT INTO pengantaran (id_donasi, id_penerima, id_relawan, status_pengantaran, tanggal_pengantaran) VALUES
(3, 3, 5, 'diantar', CURRENT_DATE);

-- 5. Insert Laporan Masalah
INSERT INTO laporan_masalah (id_donasi, id_pelapor, isi_laporan, status_laporan) VALUES
(3, 3, 'Waktu penjemputan agak terlambat karena kendala hujan deras di jalan.', 'diproses');

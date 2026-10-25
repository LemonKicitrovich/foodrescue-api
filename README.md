# FoodRescue API - Tugas Akhir Backend Development

> **Nama**  : Raihan Noviansyah  
> **NIM**   : 21114012610124  
> **Mata Kuliah** : Learning Labs: Backend Development  
> **Tema Project** : FoodRescue (Platform Penyelamatan dan Donasi Makanan Berlebih)  

---

## 1. Deskripsi Project

**FoodRescue API** adalah layanan REST API yang dibangun untuk memfasilitasi pendistribusian makanan berlebih yang masih layak konsumsi agar tidak terbuang sia-sia (*food waste*). 

Sistem ini menghubungkan 4 pihak utama:
1. **Donatur** (Restoran, katering, toko roti, hotel, atau perorangan) yang ingin mendonasikan makanan berlebih.
2. **Penerima** (Panti asuhan, komunitas sosial, warga pra-sejahtera, yayasan lansia) yang membutuhkan bantuan makanan.
3. **Relawan** yang bertugas memeriksa kelayakan makanan (*quality check*) serta mengantarkan makanan ke lokasi penerima.
4. **Admin** yang memantau kelancaran alur dan menangani laporan masalah dari pengguna.

API ini dibangun menggunakan framework **Python Flask**, ORM **Flask-SQLAlchemy**, dan database **PostgreSQL** yang di-deploy secara *serverless* di **Vercel**.

---

## 2. Link Deployment & Repository

- **Repository GitHub** : `https://github.com/raihannoviansyah/foodrescue-api` *(isi dengan link repo kalian)*
- **Live Deployment Vercel** : `https://foodrescue-api.vercel.app` *(isi dengan domain vercel yang didapat)*
- **Dokumentasi API / Collection** : `FoodRescue_API_Postman_Collection.json`

---

## 3. Skema Database & ERD

Database terdiri dari **5 tabel utama** yang saling berelasi menggunakan Foreign Key:

1. `pengguna` : Menyimpan data seluruh akun pengguna (donatur, penerima, relawan, admin).
2. `donasi` : Menyimpan data makanan yang didonasikan oleh donatur.
3. `pemeriksaan_makanan` : Menyimpan hasil verifikasi kelayakan makanan oleh relawan/admin (*one-to-one* dengan donasi).
4. `pengantaran` : Menyimpan proses distribusi makanan dari donatur ke penerima oleh relawan.
5. `laporan_masalah` : Menyimpan tiket laporan jika terjadi kendala pada donasi atau pengiriman.

### Diagram Relasi (ERD)

```
pengguna (1) ──────────< (N) donasi (1) ────────── (1) pemeriksaan_makanan
   │                            │
   │                            ├──< (N) pengantaran (N) ────────── (1) pengguna (penerima/relawan)
   │                            │
   └──────────< (N) laporan_masalah (N) ────────── (1) donasi
```

#### Format dbdiagram.io (Bisa dicopy langsung ke dbdiagram.io)
```dbml
Table pengguna {
  id_pengguna integer [pk, increment]
  nama varchar(100) [not null]
  email varchar(100) [unique, not null]
  nomor_hp varchar(20)
  alamat text
  peran varchar(20) [note: 'donatur, penerima, relawan, admin']
}

Table donasi {
  id_donasi integer [pk, increment]
  id_donatur integer [not null, ref: > pengguna.id_pengguna]
  nama_makanan varchar(100) [not null]
  jumlah integer [not null]
  lokasi_pengambilan text [not null]
  tanggal_kadaluarsa date [not null]
  status varchar(20) [default: 'tersedia', note: 'tersedia, dipesan, selesai, dibatalkan']
}

Table pemeriksaan_makanan {
  id_pemeriksaan integer [pk, increment]
  id_donasi integer [unique, not null, ref: - donasi.id_donasi]
  id_pemeriksa integer [not null, ref: > pengguna.id_pengguna]
  kondisi varchar(20) [note: 'layak, tidak layak']
  catatan text
}

Table pengantaran {
  id_pengantaran integer [pk, increment]
  id_donasi integer [not null, ref: > donasi.id_donasi]
  id_penerima integer [not null, ref: > pengguna.id_pengguna]
  id_relawan integer [ref: > pengguna.id_pengguna]
  status_pengantaran varchar(20) [default: 'menunggu', note: 'menunggu, diambil, diantar, selesai']
  tanggal_pengantaran date
}

Table laporan_masalah {
  id_laporan integer [pk, increment]
  id_donasi integer [not null, ref: > donasi.id_donasi]
  id_pelapor integer [not null, ref: > pengguna.id_pengguna]
  isi_laporan text [not null]
  status_laporan varchar(20) [default: 'belum ditangani', note: 'belum ditangani, diproses, selesai']
}
```

---

## 4. Cara Menjalankan Project Secara Lokal

### Prasyarat
- Python 3.10+
- Git
- PostgreSQL (atau bisa pakai SQLite default saat di lokal)

### Langkah-langkah
1. **Clone repository ini:**
   ```bash
   git clone https://github.com/raihannoviansyah/foodrescue-api.git
   cd foodrescue-api
   ```

2. **Buat dan aktifkan Virtual Environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment Variable:**
   Copy file `.env.example` menjadi `.env`:
   ```bash
   cp .env.example .env
   ```
   Sesuaikan `DATABASE_URL` jika ingin menghubungkan ke database PostgreSQL lokal atau Supabase.

5. **Jalankan Aplikasi:**
   ```bash
   python run.py
   ```
   Aplikasi akan berjalan di: `http://localhost:5000`

---

## 5. Dokumentasi Endpoint API

Base URL: `http://localhost:5000` atau URL Vercel `https://foodrescue-api.vercel.app`

---

### A. Resource: Donasi (CRUD Lengkap)

#### 1. Mengambil Semua Donasi Makanan
- **Method** : `GET`
- **URL** : `/donasi` (atau `/donasi?status=tersedia`)
- **Deskripsi** : Mengambil semua data donasi makanan yang terdaftar.
- **Headers** : Tidak ada
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data donasi berhasil diambil",
    "data": [
      {
        "id_donasi": 1,
        "id_donatur": 1,
        "nama_donatur": "Restoran Padang Minang Saiyo",
        "nama_makanan": "Nasi Kotak Rendang & Ayam Gulai",
        "jumlah": 25,
        "lokasi_pengambilan": "Restoran Padang Minang Saiyo, Jl. Merdeka 45",
        "tanggal_kadaluarsa": "2026-10-26",
        "status": "tersedia"
      }
    ]
  }
  ```

#### 2. Mengambil Detail Donasi Berdasarkan ID
- **Method** : `GET`
- **URL** : `/donasi/1`
- **Deskripsi** : Melihat informasi lengkap satu donasi makanan tertentu.
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Detail donasi ditemukan",
    "data": {
      "id_donasi": 1,
      "id_donatur": 1,
      "nama_donatur": "Restoran Padang Minang Saiyo",
      "nama_makanan": "Nasi Kotak Rendang & Ayam Gulai",
      "jumlah": 25,
      "lokasi_pengambilan": "Restoran Padang Minang Saiyo, Jl. Merdeka 45",
      "tanggal_kadaluarsa": "2026-10-26",
      "status": "tersedia"
    }
  }
  ```
- **Response Error (404 Not Found)** :
  ```json
  {
    "status": "error",
    "error": "Donasi dengan ID 999 tidak ditemukan"
  }
  ```

#### 3. Mendaftarkan Donasi Makanan Baru
- **Method** : `POST`
- **URL** : `/donasi`
- **Deskripsi** : Donatur menambahkan stok makanan berlebih untuk disumbangkan.
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "id_donatur": 1,
    "nama_makanan": "Nasi Box Ayam Bakar & Lalapan",
    "jumlah": 30,
    "lokasi_pengambilan": "Restoran Padang Minang Saiyo, Jl. Merdeka 45",
    "tanggal_kadaluarsa": "2026-11-01",
    "status": "tersedia"
  }
  ```
- **Response Sukses (201 Created)** :
  ```json
  {
    "status": "success",
    "message": "Donasi makanan berhasil didaftarkan",
    "data": {
      "id_donasi": 4,
      "id_donatur": 1,
      "nama_donatur": "Restoran Padang Minang Saiyo",
      "nama_makanan": "Nasi Box Ayam Bakar & Lalapan",
      "jumlah": 30,
      "lokasi_pengambilan": "Restoran Padang Minang Saiyo, Jl. Merdeka 45",
      "tanggal_kadaluarsa": "2026-11-01",
      "status": "tersedia"
    }
  }
  ```
- **Response Error (400 Bad Request)** :
  ```json
  {
    "status": "error",
    "error": "Field 'nama_makanan' wajib diisi"
  }
  ```

#### 4. Memperbarui Data / Status Donasi
- **Method** : `PUT` / `PATCH`
- **URL** : `/donasi/1`
- **Deskripsi** : Mengubah jumlah makanan, lokasi, atau status ketersediaan donasi.
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "jumlah": 35,
    "status": "tersedia"
  }
  ```
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data donasi berhasil diperbarui",
    "data": {
      "id_donasi": 1,
      "id_donatur": 1,
      "nama_makanan": "Nasi Kotak Rendang & Ayam Gulai",
      "jumlah": 35,
      "lokasi_pengambilan": "Restoran Padang Minang Saiyo, Jl. Merdeka 45",
      "tanggal_kadaluarsa": "2026-10-26",
      "status": "tersedia"
    }
  }
  ```

#### 5. Menghapus Data Donasi
- **Method** : `DELETE`
- **URL** : `/donasi/2`
- **Deskripsi** : Menghapus data donasi makanan yang batal atau kadaluarsa.
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Donasi dengan ID 2 berhasil dihapus"
  }
  ```

---

### B. Resource: Pengguna

#### 1. Mengambil Daftar Semua Pengguna
- **Method** : `GET`
- **URL** : `/pengguna` (opsional: `/pengguna?peran=donatur`)
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data pengguna berhasil diambil",
    "data": [
      {
        "id_pengguna": 1,
        "nama": "Restoran Padang Minang Saiyo",
        "email": "admin@minangsaiyo.com",
        "nomor_hp": "081234567890",
        "alamat": "Jl. Merdeka No. 45, Jakarta Pusat",
        "peran": "donatur"
      }
    ]
  }
  ```

#### 2. Mendaftarkan Pengguna Baru
- **Method** : `POST`
- **URL** : `/pengguna`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "nama": "Catering Berkah Jaya",
    "email": "kontak@cateringberkah.com",
    "nomor_hp": "081299881122",
    "alamat": "Jl. Fatmawati No. 50, Jakarta Selatan",
    "peran": "donatur"
  }
  ```
- **Response Sukses (201 Created)** :
  ```json
  {
    "status": "success",
    "message": "Pengguna berhasil didaftarkan",
    "data": {
      "id_pengguna": 8,
      "nama": "Catering Berkah Jaya",
      "email": "kontak@cateringberkah.com",
      "nomor_hp": "081299881122",
      "alamat": "Jl. Fatmawati No. 50, Jakarta Selatan",
      "peran": "donatur"
    }
  }
  ```

#### 3. Update Profil Pengguna
- **Method** : `PUT`
- **URL** : `/pengguna/1`
- **Request Body** :
  ```json
  {
    "nomor_hp": "081299889988",
    "alamat": "Jl. Fatmawati No. 88, Jakarta Selatan"
  }
  ```
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data pengguna berhasil diperbarui"
  }
  ```

#### 4. Hapus Pengguna
- **Method** : `DELETE`
- **URL** : `/pengguna/8`
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Pengguna ID 8 berhasil dihapus"
  }
  ```

---

### C. Resource: Pemeriksaan Makanan (Quality Check)

#### 1. Mengambil Semua Riwayat Pemeriksaan
- **Method** : `GET`
- **URL** : `/pemeriksaan`
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data pemeriksaan makanan berhasil diambil",
    "data": [
      {
        "id_pemeriksaan": 1,
        "id_donasi": 1,
        "nama_makanan": "Nasi Kotak Rendang & Ayam Gulai",
        "id_pemeriksa": 5,
        "nama_pemeriksa": "Budi Santoso",
        "kondisi": "layak",
        "catatan": "Kemasan higienis, porsi baru dimasak sore hari dan masih hangat."
      }
    ]
  }
  ```

#### 2. Input Hasil Pemeriksaan Kualitas Makanan
- **Method** : `POST`
- **URL** : `/pemeriksaan`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "id_donasi": 3,
    "id_pemeriksa": 5,
    "kondisi": "layak",
    "catatan": "Kemasan tersegel aman, suhu makanan terjaga, layak konsumsi."
  }
  ```
- **Response Sukses (201 Created)** :
  ```json
  {
    "status": "success",
    "message": "Pemeriksaan makanan berhasil disimpan",
    "data": {
      "id_pemeriksaan": 3,
      "id_donasi": 3,
      "id_pemeriksa": 5,
      "kondisi": "layak",
      "catatan": "Kemasan tersegel aman, suhu makanan terjaga, layak konsumsi."
    }
  }
  ```

---

### D. Resource: Pengantaran Makanan

#### 1. Mengambil Daftar Pengantaran
- **Method** : `GET`
- **URL** : `/pengantaran`
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Data pengantaran berhasil diambil",
    "data": [
      {
        "id_pengantaran": 1,
        "id_donasi": 3,
        "nama_makanan": "Lauk Ikan Bakar & Sayur Nangka",
        "id_penerima": 3,
        "nama_penerima": "Panti Asuhan Kasih Bunda",
        "id_relawan": 5,
        "nama_relawan": "Budi Santoso",
        "status_pengantaran": "diantar",
        "tanggal_pengantaran": "2026-10-25"
      }
    ]
  }
  ```

#### 2. Membuat Pesanan Pengantaran Donasi
- **Method** : `POST`
- **URL** : `/pengantaran`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "id_donasi": 1,
    "id_penerima": 3,
    "id_relawan": 5
  }
  ```
- **Response Sukses (201 Created)** :
  ```json
  {
    "status": "success",
    "message": "Pesanan pengantaran donasi berhasil dibuat"
  }
  ```

#### 3. Memperbarui Status Pengantaran
- **Method** : `PUT`
- **URL** : `/pengantaran/1`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "status_pengantaran": "selesai"
  }
  ```
- **Response Sukses (200 OK)** :
  ```json
  {
    "status": "success",
    "message": "Status pengantaran berhasil diperbarui"
  }
  ```

---

### E. Resource: Laporan Masalah

#### 1. Mengambil Seluruh Laporan
- **Method** : `GET`
- **URL** : `/laporan`
- **Response Sukses (200 OK)**

#### 2. Membuat Laporan Kendala Donasi
- **Method** : `POST`
- **URL** : `/laporan`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "id_donasi": 1,
    "id_pelapor": 3,
    "isi_laporan": "Jumlah makanan yang diterima kurang 2 porsi dari info awal."
  }
  ```
- **Response Sukses (201 Created)**

#### 3. Update Penanganan Laporan Masalah
- **Method** : `PUT`
- **URL** : `/laporan/1`
- **Headers** : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "status_laporan": "selesai"
  }
  ```
- **Response Sukses (200 OK)**

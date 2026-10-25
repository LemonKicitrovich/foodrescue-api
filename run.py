from app import create_app
from app.extensions import db

app = create_app()

# Perintah opsional untuk membuat tabel otomatis saat pertama kali run jika belum ada
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        # Jika database belum terkoneksi saat build time vercel, abaikan agar tidak crash
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

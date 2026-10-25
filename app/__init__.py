from flask import Flask, jsonify
from app.config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi Database
    db.init_app(app)

    # Register Blueprints
    from app.routes.donasi import donasi_bp
    from app.routes.pengguna import pengguna_bp
    from app.routes.pemeriksaan import pemeriksaan_bp
    from app.routes.pengantaran import pengantaran_bp
    from app.routes.laporan import laporan_bp

    app.register_blueprint(donasi_bp)
    app.register_blueprint(pengguna_bp)
    app.register_blueprint(pemeriksaan_bp)
    app.register_blueprint(pengantaran_bp)
    app.register_blueprint(laporan_bp)

    # Endpoint Index / Home
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "project": "FoodRescue REST API",
            "author": "Raihan Noviansyah",
            "nim": "21114012610124",
            "status": "online",
            "description": "API Backend untuk menghubungkan donatur makanan berlebih dengan penerima yang membutuhkan.",
            "endpoints": {
                "pengguna": "/pengguna",
                "donasi": "/donasi",
                "pemeriksaan": "/pemeriksaan",
                "pengantaran": "/pengantaran",
                "laporan": "/laporan"
            }
        }), 200

    # Handler 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "error": "Endpoint tidak ditemukan"
        }), 404

    # Handler 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "error": "Terjadi kesalahan internal pada server"
        }), 500

    return app

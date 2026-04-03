from flask import Flask, jsonify
from app.database import init_db
from app.auth import auth_bp
from app.products import products_bp
from app.orders import orders_bp
from app.payments import payments_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev_secret_key"

    init_db()

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(orders_bp, url_prefix="/api")
    app.register_blueprint(payments_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({
            "app": "ShopSecure E-Commerce API",
            "version": "1.0.0",
            "endpoints": [
                "POST /api/register",
                "POST /api/login",
                "GET  /api/products",
                "POST /api/orders",
                "POST /api/payments"
            ]
        })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
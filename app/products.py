from flask import Blueprint, request, jsonify
from app.models import Product
from app.auth import verify_token

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.get_all()
    return jsonify([dict(p) for p in products]), 200

@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product)), 200

@products_bp.route("/products/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "")
    results = Product.search(query)
    return jsonify([dict(p) for p in results]), 200

@products_bp.route("/products", methods=["POST"])
def create_product():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user or user.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    Product.create(
        data["name"],
        data.get("description", ""),
        data["price"],
        data.get("stock", 0),
        data.get("category", "general")
    )
    return jsonify({"message": "Product created"}), 201
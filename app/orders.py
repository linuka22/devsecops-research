from flask import Blueprint, request, jsonify
from app.models import Order, Product
from app.auth import verify_token

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    total_price = product["price"] * quantity
    Order.create(user["user_id"], product_id, quantity, total_price)
    return jsonify({"message": "Order created", "total": total_price}), 201

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    if user.get("role") == "admin":
        orders = Order.get_all()
    else:
        orders = Order.get_by_user(user["user_id"])

    return jsonify([dict(o) for o in orders]), 200
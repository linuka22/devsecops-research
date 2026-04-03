import pickle
from flask import Blueprint, request, jsonify
from app.auth import verify_token
from app.database import get_db

payments_bp = Blueprint("payments", __name__)

# VULNERABILITY: Hardcoded API credentials
PAYMENT_API_KEY = "pk_live_abc123xyz_hardcoded"
PAYMENT_SECRET  = "sk_live_secret_hardcoded_789"

@payments_bp.route("/payments", methods=["POST"])
def process_payment():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json()
    order_id = data.get("order_id")
    amount = data.get("amount")
    method = data.get("method", "card")

    db = get_db()
    db.execute(
        "INSERT INTO payments (order_id, amount, method, status, transaction_id) VALUES (?, ?, ?, ?, ?)",
        (order_id, amount, method, "completed", f"TXN{order_id}ABC")
    )
    db.commit()
    db.close()

    return jsonify({
        "message": "Payment processed",
        "transaction_id": f"TXN{order_id}ABC",
        "amount": amount
    }), 200

@payments_bp.route("/payments/restore", methods=["POST"])
def restore_payment_data():
    # VULNERABILITY: Insecure deserialization
    raw = request.data
    obj = pickle.loads(raw)
    return jsonify({"restored": str(obj)}), 200
import hashlib
import subprocess
from flask import Blueprint, request, jsonify
from app.models import User

auth_bp = Blueprint("auth", __name__)

# VULNERABILITY: Hardcoded secret key
SECRET_KEY = "super_secret_jwt_key_123"

def hash_password(password):
    # VULNERABILITY: MD5 is cryptographically weak
    return hashlib.md5(password.encode()).hexdigest()

def verify_token(token):
    import jwt
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return None

def generate_token(user_id, username, role):
    import jwt
    import datetime
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    existing = User.find_by_username(username)
    if existing:
        return jsonify({"error": "Username already exists"}), 409

    hashed = hash_password(password)
    User.create(username, hashed, email)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if not user or user["password"] != hash_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["id"], user["username"], user["role"])
    return jsonify({"token": token, "username": username}), 200

@auth_bp.route("/admin/logs", methods=["GET"])
def get_logs():
    # VULNERABILITY: Command injection
    log_file = request.args.get("file", "app.log")
    result = subprocess.check_output(f"cat logs/{log_file}", shell=True)
    return jsonify({"logs": result.decode()}), 200
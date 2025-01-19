from flask import Blueprint, jsonify, request
from app.auth import login, logout
from app.utils.decorators import login_required

# 创建Blueprint
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def user_login():
    """
    用户登录接口
    """
    data = request.json
    username = data.get("username")
    encrypted_password = data.get("password")

    if not username or not encrypted_password:
        return jsonify({"error": "Username and password are required"}), 400

    success, message = login(username, encrypted_password)
    if not success:
        return jsonify({"error": message}), 401
    return jsonify({"message": message})

@auth_bp.route("/logout", methods=["POST"])
@login_required
def user_logout():
    """
    用户登出接口
    """
    success, message = logout()
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message})
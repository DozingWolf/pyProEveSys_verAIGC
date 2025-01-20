from flask import Blueprint, jsonify, request, session
from datetime import datetime
from loguru import logger
from app.models import SessionLocal, User
from app.utils.decorators import login_required, permission_required

# 创建Blueprint
user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
@login_required
@permission_required("view_users")  # 假设需要 "view_users" 权限
def get_all_users():
    """
    查询所有用户信息的接口
    需要登录且具有 "view_users" 权限
    """
    db = SessionLocal()
    try:
        # 查询所有用户
        users = db.query(User).all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "is_active": user.is_active
            })
        return jsonify({"users": user_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@user_bp.route("/register", methods=["POST"])
def register():
    """
    用户注册接口
    """
    data = request.json
    db = SessionLocal()
    try:
        # 检查当前用户是否已登录
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        # 获取当前登录用户的 empid
        createuser = session["user_id"]

        # 生成随机密码（如果未提供密码）
        password = data.get("password")
        if not password:
            password = PasswordService.generate_random_password()

        # 对密码进行加盐加密
        hashed_password = PasswordService.hash_password(password)

        # 创建用户
        new_user = User(
            empcode=data.get("empcode"),  # 用户工号
            empname=data.get("empname"),  # 用户名
            passwd=hashed_password,  # 加密后的密码
            sex=data.get("sex", 1),  # 性别，默认为1（女性）
            createuser=createuser,  # 创建人
            createdate=datetime.now(),  # 创建时间
            modifyuser=createuser,  # 修改人
            modifydate=datetime.now(),  # 修改时间
            status=0,  # 状态位，0正常
            admin=data.get("admin", 1)  # 管理员标记，默认为1（普通用户）
        )
        db.add(new_user)
        db.commit()

        return jsonify({"message": "User registered successfully", "user_id": new_user.empid})
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()
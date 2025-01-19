from flask import Blueprint, jsonify
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
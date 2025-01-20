import os
import random
import string
from flask import Blueprint, jsonify
from app.models import SessionLocal, User  # 使用绝对导入
from app.config import Config  # 使用绝对导入
from app.utils.crypto import PasswordService  # 使用绝对导入
from loguru import logger

# 创建Blueprint
init_bp = Blueprint("init", __name__)

def generate_random_password(length=8):
    """
    生成随机密码
    """
    characters = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choice(characters) for _ in range(length))

@init_bp.route("/init_admin", methods=["POST"])
def init_admin():
    """
    初始化管理员用户接口
    """
    db = SessionLocal()
    try:
        # 检查是否已经存在管理员用户
        admin_user = db.query(User).filter(User.empcode == "ADM0000").first()
        if admin_user:
            logger.warning("Admin user already exists")
            return jsonify({"error": "Admin user already exists"}), 400

        # 生成随机密码
        password = generate_random_password()
        logger.info(f"Generated admin password: {password}")

        # 对密码进行加盐加密
        hashed_password = PasswordService.hash_password(password)  # 使用 crypto.py 中的方法
        logger.info(f"Hashed admin password: {hashed_password}")

        # 创建管理员用户
        admin_user = User(
            empid=0,  # 用户内码
            empcode="ADM0000",  # 用户工号
            empname="系统管理员",  # 用户名
            passwd=hashed_password,  # 加盐加密后的密码
            sex=0,  # 性别，0男性
            createuser=0,  # 创建人内码（系统）
            status=0,  # 状态位，0正常
            admin=0  # 管理员标记，0管理员
        )
        db.add(admin_user)
        db.commit()

        # 将明文密码保存到文件（仅用于初始化，后续应删除或妥善保管）
        password_file_path = os.path.join(Config.BASE_DIR, "app", "admin_password.txt")
        os.makedirs(os.path.dirname(password_file_path), exist_ok=True)  # 确保目录存在
        with open(password_file_path, "w") as f:
            f.write(password)
        logger.info(f"Admin password saved to {password_file_path}")

        return jsonify({"message": "Admin user created successfully", "password": password})
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating admin user: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()
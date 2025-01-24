from flask import Blueprint, session, make_response, jsonify, request
from PIL import Image, ImageDraw, ImageFont
import random
import io
import string  # 导入 string 模块
from app.models import SessionLocal,User  # 导入 SessionLocal
from app.utils.crypto import PasswordService
from loguru import logger
from app.auth import login, logout
from app.utils.decorators import login_required

# 创建Blueprint
auth_bp = Blueprint("auth", __name__)

def generate_captcha_text(length=4):
    """
    生成验证码文本（四位大写字母和数字）
    """
    characters = string.ascii_uppercase + string.digits  # 大写字母和数字
    return ''.join(random.choice(characters) for _ in range(length))

def generate_captcha_image(captcha_text):
    """
    生成验证码图片
    """
    # 创建图片
    image = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # 绘制验证码文本
    draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

    # 将图片转换为字节流
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@auth_bp.route("/captcha", methods=["GET"])
def get_captcha():
    """
    获取验证码图片接口
    """
    try:
        # 生成验证码文本
        captcha_text = generate_captcha_text()

        # 对验证码进行加密并存储到 session 中
        encrypted_captcha = PasswordService.hash_password(captcha_text)
        session["captcha"] = encrypted_captcha

        # 生成验证码图片
        image_buffer = generate_captcha_image(captcha_text)

        # 返回验证码图片
        response = make_response(image_buffer.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response
    except Exception as e:
        logger.error(f"Error generating captcha: {e}")
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    用户登录接口（包含验证码校验）
    """
    data = request.json
    db = SessionLocal()
    try:
        # 检查验证码
        if "captcha" not in session:
            return jsonify({"error": "Captcha not generated"}), 400

        # 解密验证码
        encrypted_captcha = session["captcha"]
        user_captcha = data.get("captcha")
        if not PasswordService.verify_password(user_captcha, encrypted_captcha):
            return jsonify({"error": "Invalid captcha"}), 400

        # 检查用户名和密码
        username = data.get("username")
        password = data.get("password")
        user = db.query(User).filter(User.empcode == username).first()
        if not user or not PasswordService.verify_password(password, user.passwd):
            return jsonify({"error": "Invalid username or password"}), 401

        # 设置 Session
        session["user_id"] = user.empid
        logger.info(f"User {username} logged in successfully")
        return jsonify({"message": "Login successful"})
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

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
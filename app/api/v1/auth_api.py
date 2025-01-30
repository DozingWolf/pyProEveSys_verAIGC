from flask import Blueprint, session, make_response, jsonify, request
from PIL import Image, ImageDraw, ImageFont
import random
import io
import string  # 导入 string 模块
from app.models import SessionLocal,User  # 导入 SessionLocal
import configparser
from app.utils.crypto import PasswordService
import datetime

# 加载配置文件
config = configparser.ConfigParser()
config.read('conf.ini')
PRIVATE_KEY = config['rsa']['private_key']
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

    参数:
        empcode (str): 用户工号
        password (str): 加密后的密码
        captcha (str): 验证码

    返回:
        dict: 登录结果
    """
    try:
        data = request.json
        db = SessionLocal()

        # 验证验证码
        if "captcha" not in session:
            return jsonify({"error": "验证码未生成"}), 400

        user_captcha = data.get("captcha")
        if not user_captcha.lower() != session["captcha"].lower():
            logger.debug(data.get("captcha"))
            logger.debug(user_captcha)
            return jsonify({"error": "验证码错误"}), 400

        # 验证用户是否存在
        empcode = data.get("empcode")
        user = db.query(User).filter(User.empcode == empcode).first()
        if not user:
            return jsonify({"error": "用户不存在"}), 404

        # 验证密码
        encrypted_password = data.get("password")
        try:
                decrypted_password = PasswordService.decrypt_rsa(encrypted_password, PRIVATE_KEY)
        except Exception as e:
            logger.error(f"RSA解密失败: {e}")
            return jsonify({"error": "密码解密失败"}), 400

        if not PasswordService.verify_password(decrypted_password, user.passwd):
            return jsonify({"error": "密码错误"}), 401

        # 登录成功，设置 session
        session["login_status"] = True
        session["empcode"] = user.empcode
        session["empid"] = user.empid
        session["login_time"] = datetime.datetime.now().isoformat()
        logger.info(f"用户 {empcode} 登录成功")
        return jsonify({"message": "登录成功"})
    except Exception as e:
        logger.error(f"登录错误: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

@auth_bp.route("/logout", methods=["POST"])
@login_required
def user_logout():
    """
    用户登出接口

    返回:
        dict: 登出结果
    """
    try:
        if "login_status" not in session or not session["login_status"]:
            return jsonify({"error": "用户尚未登录，无法登出"}), 400

        # 清除登录状态
        session.pop("login_status", None)
        session.pop("empcode", None)
        session.pop("empid", None)
        session.pop("login_time", None)
        logger.info("用户登出成功")
        return jsonify({"message": "登出成功"})
    except Exception as e:
        logger.error(f"登出错误: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

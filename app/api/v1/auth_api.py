from flask import Blueprint, session, make_response, jsonify, request
from app.models import SessionLocal,User  # 导入 SessionLocal
from app.utils.crypto import PasswordService
import datetime
import base64
from app.config import Config  # 导入配置类

# 加载 RSA 密钥
PRIVATE_KEY, PUBLIC_KEY = Config.load_rsa_keys()  # 获取私钥
from loguru import logger
from app.auth import login, logout
from app.utils.decorators import login_required
from app.auth import generate_captcha_text, generate_captcha_image
# 创建Blueprint
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/captcha", methods=["GET"])
def get_captcha():
    """
    获取验证码图片接口
    ---
    get:
      tags:
        - 认证管理
      summary: 获取验证码图片
      description: 生成并返回验证码图片，同时将验证码文本存储在session中
      responses:
        200:
          description: 成功返回验证码图片
          content:
            image/png:
              schema:
                type: string
                format: binary
        500:
          description: 服务器内部错误
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Internal server error
    """
    try:
        # 生成验证码文本
        captcha_text = generate_captcha_text()

        # 将验证码文本存储到session中
        session["captcha"] = captcha_text
        
        # 生成验证码图片
        image_buffer = generate_captcha_image(captcha_text)

        # 返回验证码图片
        response = make_response(image_buffer.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response
    except Exception as e:
        logger.error(f"生成验证码失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

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
        logger.debug(user_captcha.lower())
        logger.debug(session["captcha"].lower())
        if not user_captcha.lower() == session["captcha"].lower():
            return jsonify({"error": "验证码错误"}), 400

        # 验证用户是否存在
        empcode = data.get("empcode")
        user = db.query(User).filter(User.empcode == empcode).first()
        if not user:
            return jsonify({"error": "用户不存在"}), 404

        # 验证密码
        encrypted_password = data.get("password")
        logger.debug('web encrypted password is: ')
        logger.debug(encrypted_password)
        logger.debug('============================')
        try:
            decrypted_password = PasswordService.decrypt_rsa(encrypted_password, PRIVATE_KEY)  # 使用密钥字符串
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

# @auth_bp.route("/simple_login", methods=["POST"])
# def simple_login():
#     """
#     简易用户登录接口

#     参数:
#         username (str): 用户名
#         captcha (str): 验证码
#         password (str): 密码明文

#     返回:
#         dict: 登录结果
#     """
#     try:
#         data = request.json
#         db = SessionLocal()

#         # 验证验证码
#         if "captcha" not in session:
#             return jsonify({"error": "验证码未生成"}), 400

#         user_captcha = data.get("captcha")
#         if not user_captcha.lower() == session["captcha"].lower():
#             return jsonify({"error": "验证码错误"}), 400

#         # 验证用户是否存在
#         empcode = data.get("empcode")
#         user = db.query(User).filter(User.empcode == empcode).first()
#         if not user:
#             return jsonify({"error": "用户不存在"}), 404

#         # 验证密码
#         plain_password = data.get("password")
#         if not PasswordService.verify_password(plain_password, user.passwd):
#             return jsonify({"error": "密码错误"}), 401

#         # 登录成功，设置 session
#         session["login_status"] = True
#         session["empcode"] = user.empcode
#         session["login_time"] = datetime.datetime.now().isoformat()
#         logger.info(f"用户 {empcode} 登录成功")
#         return jsonify({"message": "登录成功"})
#     except Exception as e:
#         logger.error(f"登录错误: {e}")
#         return jsonify({"error": "服务器内部错误"}), 500
#     finally:
#         db.close()

@auth_bp.route("/logout", methods=["POST"])
@login_required
def user_logout():
    """
    用户登出接口
    ---
    post:
      tags:
        - 认证管理
      summary: 用户登出
      description: 注销当前登录用户，清除会话信息
      responses:
        200:
          description: 登出成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: 登出成功
        400:
          description: 用户未登录
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: 用户尚未登录，无法登出
        500:
          description: 服务器内部错误
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: 服务器内部错误
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

# 定义需要生成文档的路由
auth_routes = [
    (get_captcha, "get_captcha"),
    (login, "login"),
    (user_logout, "user_logout")
]
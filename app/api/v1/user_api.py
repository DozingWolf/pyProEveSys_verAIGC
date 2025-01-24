from flask import Blueprint, request, session, jsonify
from datetime import datetime
from app.models import SessionLocal, User
from app.utils.crypto import PasswordService
from app.schemas.user_schema import UserSchema  # 引入 UserSchema
from flask_apispec import use_kwargs, marshal_with  # 引入 Flask-APISpec 装饰器
from loguru import logger

# 创建Blueprint
user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
@use_kwargs(UserSchema)  # 使用 UserSchema 校验请求参数
def register(**kwargs):
    """
    用户注册接口
    ---
    post:
      tags:
        - 用户管理
      summary: 注册新用户
      description: 创建一个新用户，并返回用户 ID。
      requestBody:
        required: true
        content:
          application/json:
            schema: UserSchema
      responses:
        200:
          description: 用户注册成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "User registered successfully"
                  user_id:
                    type: integer
                    example: 1
        400:
          description: 请求参数错误
        401:
          description: 未授权访问
        500:
          description: 服务器内部错误
    """
    data = request.json
    db = SessionLocal()
    try:
        # 检查当前用户是否已登录
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        # 获取当前登录用户的 empid
        createuser = session["user_id"]

        # 对密码进行加盐加密
        hashed_password = PasswordService.hash_password(data["password"])

        # 创建用户
        new_user = User(
            empcode=data["empcode"],  # 用户工号
            empname=data["empname"],  # 用户名
            passwd=hashed_password,  # 加密后的密码
            sex=data["sex"],  # 性别
            createuser=createuser,  # 创建人
            createdate=datetime.now(),  # 创建时间
            modifyuser=createuser,  # 修改人
            modifydate=datetime.now(),  # 修改时间
            status=0,  # 状态位，0正常
            admin=data["admin"]  # 管理员标记
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
from flask import Blueprint, request, session, jsonify
from datetime import datetime
from app.models import SessionLocal, User
from app.utils.crypto import PasswordService
from app.schemas.user_schema import UserSchema, EditUserSchema, UpdatePasswdSchema  # 引入所需Schema
from flask import current_app  # 导入current_app以访问配置
from app.utils.crypto import PasswordService  # 导入密码服务

from app.utils.decorators import login_required  # 引入登录验证装饰器

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


@user_bp.route("/UpdatePasswd", methods=["POST"])
@login_required  # 使用登录验证装饰器
@use_kwargs(UpdatePasswdSchema)  # 使用 UpdatePasswdSchema 校验请求参数
def update_passwd(**kwargs):
    """
    修改密码接口
    ---
    post:
      tags:
        - 用户管理
      summary: 修改用户密码
      description: 允许用户修改密码，需提供当前密码和新密码。
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdatePasswdSchema
      responses:
        200:
          description: 密码修改成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Password updated successfully"
        400:
          description: 请求参数错误
        401:
          description: 未授权访问
        403:
          description: 当前密码错误
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 获取当前用户
        user_id = session["user_id"]
        user = db.query(User).filter_by(empid=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 从配置中获取私钥
        private_key = current_app.config['RSA_PRIVATE_KEY']

        # 解密当前密码和新密码
        nowpasswd = PasswordService.decrypt_rsa(kwargs['nowpasswd'], private_key)
        newpasswd = PasswordService.decrypt_rsa(kwargs['newpasswd'], private_key)

        # 验证当前密码是否正确
        if not PasswordService.verify_password(nowpasswd, user.passwd):
            return jsonify({"error": "Current password is incorrect"}), 403

        # 对新密码进行加盐加密
        hashed_password = PasswordService.hash_password(newpasswd)

        # 更新密码
        user.passwd = hashed_password
        user.modifyuser = user_id
        user.modifydate = datetime.now()

        db.commit()

        return jsonify({"message": "Password updated successfully"})
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating password: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()



@user_bp.route("/edit_user", methods=["POST"])
@login_required  # 使用登录验证装饰器
@use_kwargs(EditUserSchema)  # 使用 EditUserSchema 校验请求参数
def edit_user(empid, **kwargs):
    """
    编辑用户信息接口
    ---
    post:
      tags:
        - 用户管理
      summary: 编辑用户信息
      description: 修改指定用户的部分或全部可编辑信息。
      parameters:
        - name: empid
          in: query
          description: 用户内码
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: EditUserSchema
      responses:
        200:
          description: 用户信息修改成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "User updated successfully"
        400:
          description: 请求参数错误
        401:
          description: 未授权访问
        404:
          description: 用户不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 获取要修改的用户
        user = db.query(User).filter_by(empid=empid).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 更新用户信息
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)

        # 更新修改时间和修改人
        user.modifyuser = session["user_id"]
        user.modifydate = datetime.now()

        db.commit()

        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

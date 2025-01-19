from functools import wraps
from flask import request, session, jsonify
from ..models import SessionLocal, User, UserPermission, PermissionGroup  # 导入相关模型
from ..utils.errors import BusinessError
from loguru import logger

def login_required(f):
    """
    登录认证装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查 Session 中是否存在用户 ID
        if "user_id" not in session:
            logger.warning("User not logged in")
            return jsonify({"error": "Unauthorized"}), 401

        # 查询用户是否存在
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.empid == session["user_id"]).first()  # 使用 empid 作为用户 ID
            if not user:
                logger.warning(f"User {session['user_id']} not found")
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            return jsonify({"error": "Internal server error"}), 500
        finally:
            db.close()

        # 继续执行被装饰的函数
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission_name):
    """
    权限校验装饰器
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查 Session 中是否存在用户 ID
            if "user_id" not in session:
                logger.warning("User not logged in")
                return jsonify({"error": "Unauthorized"}), 401

            db = SessionLocal()
            try:
                # 查询用户
                user = db.query(User).filter(User.empid == session["user_id"]).first()  # 使用 empid 作为用户 ID
                if not user:
                    logger.warning(f"User {session['user_id']} not found")
                    return jsonify({"error": "User not found"}), 404

                # 查询权限组
                permission_group = db.query(PermissionGroup).filter(
                    PermissionGroup.pgroupname == permission_name
                ).first()
                if not permission_group:
                    logger.warning(f"Permission group {permission_name} not found")
                    return jsonify({"error": "Permission group not found"}), 404

                # 检查用户是否拥有该权限
                user_permission = db.query(UserPermission).filter(
                    UserPermission.empid == user.empid,
                    UserPermission.pgroupid == permission_group.pgroupid
                ).first()
                if not user_permission:
                    logger.warning(f"User {user.empid} does not have permission {permission_name}")
                    return jsonify({"error": "Forbidden"}), 403

                # 继续执行被装饰的函数
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error checking permission: {e}")
                return jsonify({"error": "Internal server error"}), 500
            finally:
                db.close()
        return decorated_function
    return decorator
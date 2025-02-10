from functools import wraps
from flask import request, session, jsonify
from ..models import SessionLocal, User, UserPermission, PermissionGroup, OperationLog  # 导入相关模型
from ..utils.errors import BusinessError
from loguru import logger
from datetime import datetime

def login_required(f):
    """
    登录认证装饰器

    功能:
        验证用户是否已登录，若未登录则返回 401 错误。
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查 Session 中是否存在登录状态
        if "login_status" not in session or not session["login_status"]:
            logger.warning("用户未登录")
            return jsonify({"error": "未授权"}), 401

        # 查询用户是否存在
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.empid == session["empid"]).first()  # 使用 empid 作为用户内码
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

    参数:
        permission_name (str): 权限名称

    功能:
        验证用户是否拥有指定权限，若无权限则返回 403 错误。
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查 Session 中是否存在登录状态
            if "login_status" not in session or not session["login_status"]:
                logger.warning("用户未登录")
                return jsonify({"error": "未授权"}), 401

            db = SessionLocal()
            try:
                # 查询用户
                user = db.query(User).filter(User.empid == session["empid"]).first()  # 使用 empid 作为用户内码
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

def operation_log(operation_name):
    """
    业务操作日志装饰器
    
    参数:
        operation_name (str): 操作名称
        
    功能:
        记录用户操作日志，包括API、操作用户、请求参数、访问时间
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            db = SessionLocal()
            try:
                # 获取操作信息
                log_data = {
                    "operation_name": operation_name,
                    "api_path": request.path,
                    "request_params": request.get_json() if request.is_json else request.args,
                    "operation_time": datetime.now(),
                    "operator_id": session.get("empid")
                }
                
                # 创建日志记录
                log_entry = OperationLog(**log_data)
                db.add(log_entry)
                db.commit()
                
                # 继续执行被装饰的函数
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error recording operation log: {e}")
                db.rollback()
                return jsonify({"error": "Internal server error"}), 500
            finally:
                db.close()
        return decorated_function
    return decorator

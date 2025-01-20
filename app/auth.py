from flask import session
from .models import SessionLocal, User
from .utils.crypto import PasswordService
from .utils.errors import BusinessError
from loguru import logger

def login(username, encrypted_password, rsa_private_key):
    """
    用户登录逻辑
    """
    db = SessionLocal()
    try:
        # 解密 RSA 加密的密码
        try:
            password = PasswordService.decrypt_rsa(encrypted_password, rsa_private_key)
        except BusinessError as e:
            logger.error(f"RSA decryption failed: {e}")
            return False, "Invalid RSA decryption"

        # 查询用户
        user = db.query(User).filter(User.empcode == username).first()  # 使用 empcode 作为用户名
        if not user:
            logger.warning(f"User {username} not found")
            return False, "User not found"

        # 校验密码
        if not PasswordService.verify_password(password, user.passwd):  # 使用新的密码校验逻辑
            logger.warning(f"Invalid password for user {username}")
            return False, "Invalid credentials"

        # 设置 Session
        session["user_id"] = user.empid  # 使用 empid 作为用户 ID
        logger.info(f"User {username} logged in successfully")
        return True, "Login successful"
    except Exception as e:
        logger.error(f"Login error: {e}")
        return False, "Internal server error"
    finally:
        db.close()

def logout():
    """
    用户登出逻辑
    """
    if "user_id" in session:
        user_id = session["user_id"]
        session.pop("user_id", None)
        logger.info(f"User {user_id} logged out successfully")
        return True, "Logout successful"
    else:
        logger.warning("Logout attempted with no active session")
        return False, "No active session"
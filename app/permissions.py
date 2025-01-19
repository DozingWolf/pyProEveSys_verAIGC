from .models import SessionLocal, UserPermission, PermissionGroup, User
from .utils.errors import BusinessError
from loguru import logger

def assign_permission_to_user(user_id, permission_name):
    """
    为用户分配权限
    """
    db = SessionLocal()
    try:
        # 查询用户和权限组
        user = db.query(User).filter(User.empid == user_id).first()  # 使用 empid 作为用户 ID
        if not user:
            logger.warning(f"User {user_id} not found")
            return False, "User not found"

        permission_group = db.query(PermissionGroup).filter(PermissionGroup.pgroupname == permission_name).first()
        if not permission_group:
            logger.warning(f"Permission group {permission_name} not found")
            return False, "Permission group not found"

        # 检查是否已经分配过该权限
        existing_permission = db.query(UserPermission).filter(
            UserPermission.empid == user_id,
            UserPermission.pgroupid == permission_group.pgroupid
        ).first()
        if existing_permission:
            logger.warning(f"User {user_id} already has permission {permission_name}")
            return False, "Permission already assigned"

        # 分配权限
        new_permission = UserPermission(
            empid=user_id,
            pgroupid=permission_group.pgroupid,
            createuser=user_id,  # 假设创建人是当前用户
            status=0  # 状态位，0正常
        )
        db.add(new_permission)
        db.commit()
        logger.info(f"Permission {permission_name} assigned to user {user_id}")
        return True, "Permission assigned successfully"
    except Exception as e:
        db.rollback()
        logger.error(f"Error assigning permission: {e}")
        return False, "Internal server error"
    finally:
        db.close()
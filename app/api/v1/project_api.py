from flask import Blueprint, request, jsonify
from app.models import SessionLocal, Project
from app.schemas.project_schema import ProjectCreateSchema
from app.utils.crypto import PasswordService
from loguru import logger

# 创建Blueprint
project_bp = Blueprint("project", __name__, url_prefix="/api/v1.0/BUS")

@project_bp.route("/create_project", methods=["POST"])
def create_project():
    """
    创建项目接口

    参数:
        prjcode (str): 项目编码
        prjname (str): 项目名称
        ownerid (int): 项目经理ID
        sponsorid (int): 项目发起人ID
        desc (str): 项目说明
        goal (str): 项目目标说明
        approvetime (str): 项目批准时间（格式：YYYY-MM-DD）
        expectedtime (str): 预期结束时间（格式：YYYY-MM-DD）

    返回:
        dict: 操作结果
    """
    try:
        # 校验输入参数
        data = request.json
        schema = ProjectCreateSchema()
        validated_data = schema.load(data)

        # 创建数据库会话
        db = SessionLocal()

        # 创建项目记录
        new_project = Project(
            prjcode=validated_data["prjcode"],
            prjname=validated_data["prjname"],
            ownerid=validated_data["ownerid"],
            sponsorid=validated_data["sponsorid"],
            desc=validated_data["desc"],
            goal=validated_data["goal"],
            approvetime=validated_data["approvetime"],
            expectedtime=validated_data["expectedtime"],
            createuser=1,  # 假设当前用户ID为1
        )
        db.add(new_project)
        db.commit()

        logger.info(f"项目 {validated_data['prjname']} 创建成功")
        return jsonify({"message": "项目创建成功", "project_id": new_project.prjid}), 200

    except Exception as e:
        logger.error(f"项目创建失败: {e}")
        return jsonify({"error": "项目创建失败", "details": str(e)}), 500

    finally:
        db.close()

from flask import Blueprint, request, jsonify, session
from app.models import SessionLocal, Project
from app.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema
from app.utils.crypto import PasswordService
from loguru import logger
from flask_login import login_required
from flask_apispec import use_kwargs
from datetime import datetime
# 创建Blueprint
project_bp = Blueprint("project", __name__, url_prefix="/api/v1.0/BUS")

@project_bp.route("/create_project", methods=["POST"])
@login_required
def create_project():
    """
    创建项目接口
    ---
    post:
      tags:
        - 项目管理
      summary: 创建新项目
      description: 创建一个新的项目记录
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectCreateSchema
      responses:
        200:
          description: 项目创建成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "项目创建成功"
                  project_id:
                    type: integer
                    example: 123
        400:
          description: 请求参数错误
        500:
          description: 服务器内部错误
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
            createuser=session["empid"],  # 假设当前用户ID为1
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

@project_bp.route("/update_project/<int:project_id>", methods=["POST"])
@login_required
@use_kwargs(ProjectUpdateSchema)
def update_project(project_id, **kwargs):
    """
    修改项目信息接口
    ---
    post:
      tags:
        - 项目管理
      summary: 修改项目信息
      description: 修改指定项目的信息
      parameters:
        - name: project_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectUpdateSchema'
      responses:
        200:
          description: 项目信息修改成功
        404:
          description: 项目不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 查询项目是否存在
        project = db.query(Project).filter(Project.prjid == project_id).first()
        if not project:
            return jsonify({"error": "项目不存在"}), 404

        # 更新项目信息
        if 'ownerid' in kwargs:
            project.ownerid = kwargs['ownerid']
        if 'sponsorid' in kwargs:
            project.sponsorid = kwargs['sponsorid']
        if 'desc' in kwargs:
            project.desc = kwargs['desc']
        if 'goal' in kwargs:
            project.goal = kwargs['goal']
        if 'expectedtime' in kwargs:
            project.expectedtime = datetime.strptime(kwargs['expectedtime'], "%Y-%m-%d")
        if 'status' in kwargs:
            project.status = kwargs['status']

        # 设置修改人和修改时间
        project.modifyuser = session.get("empid")
        project.modifydate = datetime.now()

        db.commit()
        logger.info(f"项目 {project_id} 信息修改成功")
        return jsonify({"message": "项目信息修改成功"}), 200

    except Exception as e:
        db.rollback()
        logger.error(f"项目信息修改失败: {e}")
        return jsonify({"error": "项目信息修改失败", "details": str(e)}), 500
    finally:
        db.close()

from flask import Blueprint, request, jsonify, session
from app.models import SessionLocal, Project, ProjectMember, User
from app.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema, ProjectQuerySchema, ProjectMemberCreateSchema, ProjectMemberRemoveSchema, ProjectMemberQuerySchema
from app.utils.crypto import PasswordService
from loguru import logger
from app.utils.decorators import login_required, operation_log
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

@project_bp.route("/query_projects", methods=["POST"])
@login_required
@use_kwargs(ProjectQuerySchema)
def query_projects(**kwargs):
    """
    查询项目信息接口
    ---
    post:
      tags:
        - 项目管理
      summary: 查询项目信息
      description: 根据条件查询项目信息，支持组合查询和模糊查询
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectQuerySchema
      responses:
        200:
          description: 查询成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Project'
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        query = db.query(Project)
        
        # 处理精确查询条件
        if kwargs.get("prjcode"):
            query = query.filter(Project.prjcode == kwargs["prjcode"])
        if kwargs.get("ownerid"):
            query = query.filter(Project.ownerid == kwargs["ownerid"])
        if kwargs.get("sponsorid"):
            query = query.filter(Project.sponsorid == kwargs["sponsorid"])
        if kwargs.get("status") is not None:
            query = query.filter(Project.status == kwargs["status"])
            
        # 处理模糊查询条件
        if kwargs.get("prjname"):
            query = query.filter(Project.prjname.ilike(f"%{kwargs['prjname']}%"))
            
        # 处理时间范围查询
        if kwargs.get("approvetime_start") and kwargs.get("approvetime_end"):
            query = query.filter(
                Project.approvetime.between(
                    kwargs["approvetime_start"], kwargs["approvetime_end"]
                )
            )
        if kwargs.get("expectedtime_start") and kwargs.get("expectedtime_end"):
            query = query.filter(
                Project.expectedtime.between(
                    kwargs["expectedtime_start"], kwargs["expectedtime_end"]
                )
            )
            
        projects = query.all()
        return jsonify([{
            "prjid": project.prjid,
            "prjcode": project.prjcode,
            "prjname": project.prjname,
            "ownerid": project.ownerid,
            "sponsorid": project.sponsorid,
            "approvetime": project.approvetime.isoformat() if project.approvetime else None,
            "expectedtime": project.expectedtime.isoformat() if project.expectedtime else None,
            "status": project.status
        } for project in projects])
        
    except Exception as e:
        logger.error(f"查询项目信息失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

@project_bp.route("/add_project_member", methods=["POST"])
@login_required
def add_project_member():
    """
    新增项目成员接口
    ---
    post:
      tags:
        - 项目管理
      summary: 新增项目成员
      description: 为指定项目新增成员，如果成员曾经被移除，则恢复其状态
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectMemberCreateSchema
      responses:
        200:
          description: 成员添加成功
        400:
          description: 参数验证失败
        404:
          description: 项目或成员不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 校验输入参数
        data = request.json
        schema = ProjectMemberCreateSchema()
        validated_data = schema.load(data)

        # 检查项目是否存在
        project = db.query(Project).filter(Project.prjid == validated_data["prjid"]).first()
        if not project:
            return jsonify({"error": "项目不存在"}), 404

        # 检查成员是否存在
        user = db.query(User).filter(User.empid == validated_data["empid"]).first()
        if not user:
            return jsonify({"error": "成员不存在"}), 404

        # 检查成员是否曾经加入过项目
        existing_member = db.query(ProjectMember).filter(
            ProjectMember.prjid == validated_data["prjid"],
            ProjectMember.empid == validated_data["empid"]
        ).first()

        if existing_member:
            # 如果成员曾经被移除，则恢复其状态
            if existing_member.status == 1:
                existing_member.status = 0
                existing_member.modifyuser = session["empid"]
                existing_member.modifydate = datetime.now()
                db.commit()
                logger.info(f"项目 {validated_data['prjid']} 成员 {validated_data['empid']} 状态已恢复")
                return jsonify({"message": "成员状态已恢复"}), 200
            else:
                return jsonify({"error": "成员已存在"}), 400
        else:
            # 创建新的项目成员记录
            new_member = ProjectMember(
                prjid=validated_data["prjid"],
                empid=validated_data["empid"],
                createuser=session["empid"],
                createdate=datetime.now(),
                status=0
            )
            db.add(new_member)
            db.commit()
            logger.info(f"项目 {validated_data['prjid']} 新增成员 {validated_data['empid']} 成功")
            return jsonify({"message": "成员添加成功"}), 200

    except Exception as e:
        db.rollback()
        logger.error(f"新增项目成员失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

@project_bp.route("/remove_project_member", methods=["POST"])
@login_required
@operation_log("移除项目成员")
@use_kwargs(ProjectMemberRemoveSchema)
def remove_project_member(**kwargs):
    """
    移除项目成员接口
    ---
    post:
      tags:
        - 项目管理
      summary: 移除项目成员
      description: 从指定项目中移除成员（逻辑删除）
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectMemberRemoveSchema
      responses:
        200:
          description: 成员移除成功
        404:
          description: 项目或成员不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 查询项目成员记录
        member = db.query(ProjectMember).filter(
            ProjectMember.prjid == kwargs["prjid"],
            ProjectMember.empid == kwargs["empid"]
        ).first()

        if not member:
            return jsonify({"error": "项目成员不存在"}), 404

        # 更新状态为1（停用）
        member.status = 1
        member.modifyuser = session.get("empid")
        member.modifydate = datetime.now()
        
        db.commit()

        logger.info(f"项目 {kwargs['prjid']} 成员 {kwargs['empid']} 已逻辑删除")
        return jsonify({"message": "成员移除成功"}), 200

    except Exception as e:
        db.rollback()
        logger.error(f"移除项目成员失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

@project_bp.route("/query_project_members", methods=["POST"])
@login_required
@use_kwargs(ProjectMemberQuerySchema)
def query_project_members(**kwargs):
    """
    查询项目成员接口
    ---
    post:
      tags:
        - 项目管理
      summary: 查询项目成员
      description: 根据条件查询项目成员信息，支持组合查询和模糊查询
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectMemberQuerySchema
      responses:
        200:
          description: 查询成功
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    prjid:
                      type: integer
                    prjcode:
                      type: string
                    prjname:
                      type: string
                    empid:
                      type: integer
                    empcode:
                      type: string
                    empname:
                      type: string
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 构建基础查询
        query = db.query(
            ProjectMember.prjid,
            Project.prjcode,
            Project.prjname,
            User.empid,
            User.empcode,
            User.empname
        ).join(
            Project, ProjectMember.prjid == Project.prjid
        ).join(
            User, ProjectMember.empid == User.empid
        ).filter(
            ProjectMember.status == 0  # 只查询状态正常的成员
        )
        
        # 处理查询条件
        if kwargs.get("empcode"):
            query = query.filter(User.empcode == kwargs["empcode"])
        if kwargs.get("empname"):
            query = query.filter(User.empname.ilike(f"%{kwargs['empname']}%"))
        if kwargs.get("prjcode"):
            query = query.filter(Project.prjcode == kwargs["prjcode"])
        if kwargs.get("prjname"):
            query = query.filter(Project.prjname.ilike(f"%{kwargs['prjname']}%"))
            
        # 执行查询
        results = query.all()
        
        # 格式化返回结果
        return jsonify([{
            "prjid": result.prjid,
            "prjcode": result.prjcode,
            "prjname": result.prjname,
            "empid": result.empid,
            "empcode": result.empcode,
            "empname": result.empname
        } for result in results])
        
    except Exception as e:
        logger.error(f"查询项目成员失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

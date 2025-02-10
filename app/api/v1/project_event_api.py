from flask import Blueprint, request, jsonify, session
from app.models import SessionLocal, Project, Event, ProjectEvent
from app.schemas.project_event_schema import ProjectEventCreateSchema
from app.utils.decorators import login_required, operation_log
from loguru import logger
from datetime import datetime
from app.schemas.project_event_schema import ProjectEventQuerySchema
from flask_apispec import use_kwargs

# 创建Blueprint
project_event_bp = Blueprint("project_event", __name__, url_prefix="/api/v1.0/BUS")

@project_event_bp.route("/add_event_to_project", methods=["POST"])
@login_required
@operation_log("添加事件到项目")
def add_event_to_project():
    """
    添加事件到项目接口
    ---
    post:
      tags:
        - 项目管理
      summary: 添加事件到项目
      description: 将指定事件添加到项目中，并建立事件之间的层级关系
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectEventCreateSchema
      responses:
        200:
          description: 事件添加成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "事件添加成功"
                  project_event_id:
                    type: integer
                    example: 1
        400:
          description: 请求参数错误
        404:
          description: 项目或事件不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 校验输入参数
        data = request.json
        schema = ProjectEventCreateSchema()
        validated_data = schema.load(data)

        # 检查项目是否存在
        project = db.query(Project).filter(Project.prjid == validated_data["prjid"]).first()
        if not project:
            return jsonify({"error": "项目不存在"}), 404

        # 检查事件是否存在
        event = db.query(Event).filter(Event.eventid == validated_data["eventid"]).first()
        if not event:
            return jsonify({"error": "事件不存在"}), 404

        # 如果parentid不为0，检查父节点是否存在
        if validated_data["parentid"] != 0:
            parent_event = db.query(ProjectEvent).filter(
                ProjectEvent.leafid == validated_data["parentid"]
            ).first()
            if not parent_event:
                return jsonify({"error": "父节点不存在"}), 404
            depth = parent_event.depth + 1
        else:
            depth = 0

        # 创建项目事件关联
        new_project_event = ProjectEvent(
            prjid=validated_data["prjid"],
            eventid=validated_data["eventid"],
            leafid=ProjectEvent.get_next_leafid(db),  # 假设有一个获取下一个leafid的方法
            depth=depth,
            parentid=validated_data["parentid"],
            createuser=session["empid"],
            createdate=datetime.now(),
            status=0
        )
        db.add(new_project_event)
        db.commit()

        logger.info(f"事件 {validated_data['eventid']} 成功添加到项目 {validated_data['prjid']}")
        return jsonify({
            "message": "事件添加成功",
            "project_event_id": new_project_event.leafid
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"添加事件到项目失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

@project_event_bp.route("/query_project_events", methods=["POST"])
@login_required
@use_kwargs(ProjectEventQuerySchema)
def query_project_events(**kwargs):
    """
    查询项目事件信息接口
    ---
    post:
      tags:
        - 项目管理
      summary: 查询项目事件信息
      description: 根据项目编码或名称查询项目事件信息，返回主从结构数据
      requestBody:
        required: true
        content:
          application/json:
            schema: ProjectEventQuerySchema
      responses:
        200:
          description: 查询成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  prjcode:
                    type: string
                  prjname:
                    type: string
                  events:
                    type: array
                    items:
                      type: object
                      properties:
                        eventid:
                          type: integer
                        reporter:
                          type: integer
                        reportertime:
                          type: string
                        event:
                          type: string
                        leafid:
                          type: integer
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 构建基础查询
        query = db.query(
            Project.prjcode,
            Project.prjname,
            Event.eventid,
            Event.reporter,
            Event.reportertime,
            Event.event,
            ProjectEvent.leafid
        ).join(
            ProjectEvent, Project.prjid == ProjectEvent.prjid
        ).join(
            Event, ProjectEvent.eventid == Event.eventid
        ).filter(
            ProjectEvent.status == 0  # 只查询状态正常的记录
        )

        # 处理查询条件
        if kwargs.get("prjcode"):
            query = query.filter(Project.prjcode == kwargs["prjcode"])
        if kwargs.get("prjname"):
            query = query.filter(Project.prjname.ilike(f"%{kwargs['prjname']}%"))

        # 执行查询并排序
        results = query.order_by(ProjectEvent.depth.asc()).all()

        if not results:
            return jsonify({"error": "未找到相关项目事件信息"}), 404

        # 格式化返回结果
        response = {
            "prjcode": results[0].prjcode,
            "prjname": results[0].prjname,
            "events": [{
                "eventid": r.eventid,
                "reporter": r.reporter,
                "reportertime": r.reportertime.isoformat() if r.reportertime else None,
                "event": r.event,
                "leafid": r.leafid
            } for r in results]
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"查询项目事件信息失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close() 
from flask import Blueprint, session, request, jsonify
from app.models import SessionLocal, Event
from app.schemas.event_schema import EventCreateSchema, EventUpdateSchema, EventQuerySchema
from loguru import logger
from app.utils.decorators import login_required
from datetime import datetime
from flask_apispec import use_kwargs

# 创建Blueprint
event_bp = Blueprint("event", __name__)

@event_bp.route("/CreateEvent", methods=["POST"])
def create_event():
    """
    创建事件接口

    参数:
        reporter (int): 事件报告人ID
        event (str): 事件内容
        reportertime (str): 事件报告时间（格式：YYYY-MM-DD）

    返回:
        dict: 操作结果
    """
    try:
        # 校验输入参数
        data = request.json
        schema = EventCreateSchema()
        validated_data = schema.load(data)

        # 创建数据库会话
        db = SessionLocal()

        # 创建事件记录
        new_event = Event(
            reporter=validated_data["reporter"],
            event=validated_data["event"],
            reportertime=validated_data.get("reportertime"),
            createuser=1,  # 假设当前用户ID为1
        )
        db.add(new_event)
        db.commit()

        logger.info(f"事件 {new_event.eventid} 创建成功")
        return jsonify({"message": "事件创建成功", "event_id": new_event.eventid}), 200

    except Exception as e:
        logger.error(f"事件创建失败: {e}")
        return jsonify({"error": "事件创建失败", "details": str(e)}), 500

    finally:
        db.close()

@event_bp.route("/update_event/<int:event_id>", methods=["POST"])
@login_required
def update_event(event_id):
    """
    修改事件信息接口
    ---
    post:
      tags:
        - 事件管理
      summary: 修改事件信息
      description: 修改指定事件的信息
      parameters:
        - name: event_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: EventUpdateSchema
      responses:
        200:
          description: 事件信息修改成功
        400:
          description: 参数验证失败
        404:
          description: 事件不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 验证输入参数
        data = request.json
        schema = EventUpdateSchema()
        validated_data = schema.load(data)

        # 查询要修改的事件
        event = db.query(Event).filter(Event.eventid == event_id).first()
        if not event:
            return jsonify({"error": "事件不存在"}), 404

        # 更新事件信息
        if "event" in validated_data:
            event.event = validated_data["event"]
        if "status" in validated_data:
            event.status = validated_data["status"]
        
        # 更新修改人和修改时间
        event.modifyuser = session["empid"]
        event.modifydate = datetime.now()

        db.commit()

        logger.info(f"事件 {event_id} 信息修改成功")
        return jsonify({
            "message": "事件信息修改成功",
            "event_id": event_id
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"事件信息修改失败: {e}")
        return jsonify({"error": "事件信息修改失败", "details": str(e)}), 500
    finally:
        db.close()

@event_bp.route("/query_events", methods=["POST"])
@login_required
@use_kwargs(EventQuerySchema)
def query_events(**kwargs):
    """
    查询事件信息接口
    ---
    post:
      tags:
        - 事件管理
      summary: 查询事件信息
      description: 根据条件查询事件信息，支持组合查询和时间范围查询
      requestBody:
        required: true
        content:
          application/json:
            schema: EventQuerySchema
      responses:
        200:
          description: 查询成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Event'
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        query = db.query(Event)
        
        # 处理精确查询条件
        if kwargs.get("reporter"):
            query = query.filter(Event.reporter == kwargs["reporter"])
        if kwargs.get("status") is not None:
            query = query.filter(Event.status == kwargs["status"])
            
        # 处理时间范围查询
        if kwargs.get("reportertime_start"):
            # 如果未传结束时间，使用当前时间作为结束时间
            end_time = kwargs.get("reportertime_end") or datetime.now().strftime("%Y-%m-%d")
            query = query.filter(
                Event.reportertime.between(
                    kwargs["reportertime_start"], end_time
                )
            )
            
        events = query.all()
        return jsonify([{
            "eventid": event.eventid,
            "reporter": event.reporter,
            "reportertime": event.reportertime.isoformat() if event.reportertime else None,
            "event": event.event,
            "status": event.status
        } for event in events])
        
    except Exception as e:
        logger.error(f"查询事件信息失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close()

# 定义需要生成文档的路由
event_routes = [
    (create_event, "create_event"),
    (update_event, "update_event"),
    (query_events, "query_events")
]


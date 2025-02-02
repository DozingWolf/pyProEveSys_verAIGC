from flask import Blueprint, request, jsonify
from app.models import SessionLocal, Event
from app.schemas.event_schema import EventCreateSchema
from loguru import logger

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

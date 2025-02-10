from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

def validate_date_format(value):
    """
    验证日期格式是否为YYYY-MM-DD
    """
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("日期格式无效，请使用YYYY-MM-DD格式")

class EventCreateSchema(Schema):
    """
    事件创建接口的输入参数校验Schema

    参数:
        reporter (int): 事件报告人ID，必须为正整数
        event (str): 事件内容，最大长度2000
        reportertime (str): 事件报告时间，格式YYYY-MM-DD（可选）
    """
    reporter = fields.Int(required=True, validate=validate.Range(min=1))
    event = fields.Str(required=True, validate=validate.Length(max=2000))
    reportertime = fields.Str(required=False, validate=validate_date_format)

class EventUpdateSchema(Schema):
    """
    事件更新接口的输入参数校验Schema

    参数:
        event (str): 事件内容，最大长度2000
        status (int): 状态位，0正常，1停用
    """
    event = fields.Str(required=False, validate=validate.Length(max=2000))
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))

class EventQuerySchema(Schema):
    """
    事件查询参数校验 Schema
    
    参数:
        reporter (int): 事件报告人ID，精确查询
        reportertime_start (str): 事件报告时间范围查询开始日期，格式YYYY-MM-DD
        reportertime_end (str): 事件报告时间范围查询结束日期，格式YYYY-MM-DD
        status (int): 状态位，0正常，1停用
    """
    reporter = fields.Int(required=False, validate=validate.Range(min=1))
    reportertime_start = fields.Str(required=False, validate=validate_date_format)
    reportertime_end = fields.Str(required=False, validate=validate_date_format)
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))

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

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

class ProjectCreateSchema(Schema):
    """
    项目创建接口的输入参数校验Schema

    参数:
        prjcode (str): 项目编码，长度1-20
        prjname (str): 项目名称，长度1-50
        ownerid (int): 项目经理ID，必须为正整数
        sponsorid (int): 项目发起人ID，必须为正整数
        desc (str): 项目说明，最大长度2000
        goal (str): 项目目标说明，最大长度1000
        approvetime (str): 项目批准时间，格式YYYY-MM-DD
        expectedtime (str): 预期结束时间，格式YYYY-MM-DD
    """
    prjcode = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    prjname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    ownerid = fields.Int(required=True, validate=validate.Range(min=1))
    sponsorid = fields.Int(required=True, validate=validate.Range(min=1))
    desc = fields.Str(required=False, validate=validate.Length(max=2000))
    goal = fields.Str(required=False, validate=validate.Length(max=1000))
    approvetime = fields.Str(required=True, validate=validate_date_format)
    expectedtime = fields.Str(required=True, validate=validate_date_format)

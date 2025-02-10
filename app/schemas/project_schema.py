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

class ProjectUpdateSchema(Schema):
    """
    项目信息更新 Schema
    
    参数:
        ownerid (int): 项目负责人ID
        sponsorid (int): 项目发起人ID
        desc (str): 项目描述
        goal (str): 项目目标
        expectedtime (str): 预期结束时间，格式YYYY-MM-DD
        status (int): 状态位，0正常，1停用
    """
    ownerid = fields.Int(required=False, validate=validate.Range(min=1))
    sponsorid = fields.Int(required=False, validate=validate.Range(min=1))
    desc = fields.Str(required=False, validate=validate.Length(max=2000))
    goal = fields.Str(required=False, validate=validate.Length(max=1000))
    expectedtime = fields.Str(required=False, validate=validate_date_format)
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))

class ProjectQuerySchema(Schema):
    """
    项目查询参数校验 Schema
    
    参数:
        prjcode (str): 项目编码，精确查询
        prjname (str): 项目名称，模糊查询
        ownerid (int): 项目经理ID，精确查询
        sponsorid (int): 项目发起人ID，精确查询
        approvetime_start (str): 项目批准时间范围查询开始日期，格式YYYY-MM-DD
        approvetime_end (str): 项目批准时间范围查询结束日期，格式YYYY-MM-DD
        expectedtime_start (str): 预期结束时间范围查询开始日期，格式YYYY-MM-DD
        expectedtime_end (str): 预期结束时间范围查询结束日期，格式YYYY-MM-DD
        status (int): 状态位，0正常，1停用
    """
    prjcode = fields.Str(required=False)
    prjname = fields.Str(required=False)
    ownerid = fields.Int(required=False, validate=validate.Range(min=1))
    sponsorid = fields.Int(required=False, validate=validate.Range(min=1))
    approvetime_start = fields.Str(required=False, validate=validate_date_format)
    approvetime_end = fields.Str(required=False, validate=validate_date_format)
    expectedtime_start = fields.Str(required=False, validate=validate_date_format)
    expectedtime_end = fields.Str(required=False, validate=validate_date_format)
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))

class ProjectMemberCreateSchema(Schema):
    """
    项目成员创建接口的输入参数校验Schema

    参数:
        prjid (int): 项目ID，必须为正整数
        empid (int): 成员ID，必须为正整数
    """
    prjid = fields.Int(required=True, validate=validate.Range(min=1))
    empid = fields.Int(required=True, validate=validate.Range(min=1))

class ProjectMemberRemoveSchema(Schema):
    """
    移除项目成员 Schema
    
    参数:
        prjid (int): 项目ID，必须为正整数
        empid (int): 成员ID，必须为正整数
    """
    prjid = fields.Int(required=True, validate=validate.Range(min=1))
    empid = fields.Int(required=True, validate=validate.Range(min=1))

class ProjectMemberQuerySchema(Schema):
    """
    项目成员查询参数校验 Schema
    
    参数:
        empcode (str): 用户工号，精确查询
        empname (str): 用户姓名，模糊查询
        prjcode (str): 项目编码，精确查询
        prjname (str): 项目名称，模糊查询
    """
    empcode = fields.Str(required=False)
    empname = fields.Str(required=False)
    prjcode = fields.Str(required=False)
    prjname = fields.Str(required=False)

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

class CompanyCreateSchema(Schema):
    """
    公司创建接口的输入参数校验Schema

    参数:
        compcode (str): 公司编码，长度1-10
        compname (str): 公司名称，长度1-15
        compadd (str): 公司地址，最大长度30
        uscicode (str): 统一社会信用代码，最大长度20
    """
    compcode = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    compname = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    compadd = fields.Str(required=False, validate=validate.Length(max=30))
    uscicode = fields.Str(required=False, validate=validate.Length(max=20))

class CompanyUpdateSchema(Schema):
    """
    公司修改接口的输入参数校验Schema

    参数:
        compcode (str): 公司编码，长度1-10
        compname (str): 公司名称，长度1-15
        compadd (str): 公司地址，最大长度30
        uscicode (str): 统一社会信用代码，最大长度20
        status (int): 状态位，0正常，1停用
    """
    compcode = fields.Str(required=False, validate=validate.Length(min=1, max=10))
    compname = fields.Str(required=False, validate=validate.Length(min=1, max=15))
    compadd = fields.Str(required=False, validate=validate.Length(max=30))
    uscicode = fields.Str(required=False, validate=validate.Length(max=20))
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))

class CompanyQuerySchema(Schema):
    """
    公司查询参数校验 Schema
    
    参数:
        compcode (str): 公司编码，模糊查询
        compname (str): 公司名称，模糊查询
        compadd (str): 公司地址，模糊查询
        uscicode (str): 统一社会信用代码，精确查询
        createuser (int): 创建人ID，精确查询
        createdate_start (str): 创建时间范围查询开始日期，格式YYYY-MM-DD
        createdate_end (str): 创建时间范围查询结束日期，格式YYYY-MM-DD
        status (int): 状态位，0正常，1停用
    """
    compcode = fields.Str(required=False)
    compname = fields.Str(required=False)
    compadd = fields.Str(required=False)
    uscicode = fields.Str(required=False)
    createuser = fields.Int(required=False)
    createdate_start = fields.Str(required=False, validate=validate_date_format)
    createdate_end = fields.Str(required=False, validate=validate_date_format)
    status = fields.Int(required=False, validate=validate.OneOf([0, 1])) 
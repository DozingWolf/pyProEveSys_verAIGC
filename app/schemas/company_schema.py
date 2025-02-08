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
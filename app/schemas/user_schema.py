from marshmallow import Schema, fields, validate, ValidationError
from re import match

def validate_chinese_phone_number(value):
    """
    验证中国手机号码的正则表达式
    """
    pattern = r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$'
    if not match(pattern, value):
        raise ValidationError("无效的中国手机号码")

class UserSchema(Schema):
    """
    用户信息Schema
    """
    empcode = fields.Str(required=True, validate=validate.Length(min=1, max=10))  # 用户工号
    empname = fields.Str(required=True, validate=validate.Length(min=1, max=15))  # 用户名
    password = fields.Str(required=True, validate=validate.Length(min=6))  # 密码
    sex = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 性别（0男性，1女性）
    mobile = fields.Str(validate=validate_chinese_phone_number)  # 手机号码
    admin = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 管理员标记（0管理员，1普通用户）


class EditUserSchema(Schema):
    """
    编辑用户信息Schema
    
    参数:
    - empcode (str): 用户工号，长度1-10
    - empname (str): 用户名，长度1-15
    - mobile (str): 手机号码，需符合中国手机号格式
    - sex (int): 性别，0为男性，1为女性
    - admin (int): 管理员标记，0为管理员，1为普通用户
    
    返回值:
    - None
    """
    empcode = fields.Str(validate=validate.Length(min=1, max=10))  # 用户工号
    empname = fields.Str(validate=validate.Length(min=1, max=15))  # 用户名
    mobile = fields.Str(validate=validate_chinese_phone_number)  # 手机号码
    sex = fields.Int(validate=validate.OneOf([0, 1]))  # 性别（0男性，1女性）
    admin = fields.Int(validate=validate.OneOf([0, 1]))  # 管理员标记（0管理员，1普通用户）


class UpdatePasswdSchema(Schema):
    """
    修改密码Schema
    
    参数:
    - nowpasswd (str): 当前密码的RSA加密字符串
    - newpasswd (str): 新密码的RSA加密字符串
    
    返回值:
    - None
    """
    nowpasswd = fields.Str(required=True)  # 当前密码(RSA加密)
    newpasswd = fields.Str(required=True)  # 新密码(RSA加密)


class UserQuerySchema(Schema):
    """
    用户查询Schema
    
    参数:
    - empcode (str): 用户工号
    - empname (str): 用户姓名（支持模糊查询）
    - sex (int): 性别 0-女 1-男
    - mobile (str): 手机号
    - status (int): 状态 0-正常 1-停用
    - admin (int): 是否管理员 0-否 1-是
    """
    empcode = fields.Str(required=False)
    empname = fields.Str(required=False)
    sex = fields.Int(required=False, validate=validate.OneOf([0, 1]))
    mobile = fields.Str(required=False, validate=validate_chinese_phone_number)
    status = fields.Int(required=False, validate=validate.OneOf([0, 1]))
    admin = fields.Int(required=False, validate=validate.OneOf([0, 1]))

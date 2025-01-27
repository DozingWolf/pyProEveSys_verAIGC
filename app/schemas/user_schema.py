from marshmallow import Schema, fields, validate, ValidationError
from re import match

def validate_chinese_phone_number(value):
    # 中国手机号码正则表达式
    pattern = r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$'
    if not match(pattern, value):
        raise ValidationError("Invalid Chinese phone number.")

class UserSchema(Schema):
    empcode = fields.Str(required=True, validate=validate.Length(min=1, max=10))  # 用户工号
    empname = fields.Str(required=True, validate=validate.Length(min=1, max=15))  # 用户名
    password = fields.Str(required=True, validate=validate.Length(min=6))  # 密码
    sex = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 性别（0男性，1女性）
    mobile = fields.Str(validate=validate_chinese_phone_number)
    admin = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 管理员标记（0管理员，1普通用户）
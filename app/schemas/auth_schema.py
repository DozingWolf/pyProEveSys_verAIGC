from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=10))  # 用户名
    password = fields.Str(required=True, validate=validate.Length(min=6))  # 密码
    captcha = fields.Str(required=True, validate=validate.Length(min=4, max=4))  # 验证码
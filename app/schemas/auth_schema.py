from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """
    登录请求数据验证 Schema

    参数:
        empcode (str): 用户工号
        password (str): 加密后的密码
        captcha (str): 验证码
    """
    empcode = fields.Str(required=True, validate=validate.Length(min=1, max=10))  # 用户工号
    password = fields.Str(required=True, validate=validate.Length(min=6))  # 密码
    captcha = fields.Str(required=True, validate=validate.Length(min=4, max=4))  # 验证码

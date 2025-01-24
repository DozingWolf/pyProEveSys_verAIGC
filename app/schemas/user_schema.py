from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    empcode = fields.Str(required=True, validate=validate.Length(min=1, max=10))  # 用户工号
    empname = fields.Str(required=True, validate=validate.Length(min=1, max=15))  # 用户名
    password = fields.Str(required=True, validate=validate.Length(min=6))  # 密码
    sex = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 性别（0男性，1女性）
    admin = fields.Int(required=True, validate=validate.OneOf([0, 1]))  # 管理员标记（0管理员，1普通用户）
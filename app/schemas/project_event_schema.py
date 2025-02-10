from marshmallow import Schema, fields, validate

class ProjectEventCreateSchema(Schema):
    """
    项目事件关联创建接口的输入参数校验Schema

    参数:
        prjid (int): 项目ID，必须为正整数
        eventid (int): 事件ID，必须为正整数
        parentid (int): 父节点ID，必须为非负整数
    """
    prjid = fields.Int(required=True, validate=validate.Range(min=1))
    eventid = fields.Int(required=True, validate=validate.Range(min=1))
    parentid = fields.Int(required=True, validate=validate.Range(min=0)) 

class ProjectEventQuerySchema(Schema):
    """
    项目事件查询Schema
    """
    prjcode = fields.Str(required=False)  # 项目编码
    prjname = fields.Str(required=False)  # 项目名称 
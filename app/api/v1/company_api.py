from flask import Blueprint, request, jsonify, session
from app.models import SessionLocal, Company
from app.schemas.company_schema import CompanyCreateSchema, CompanyUpdateSchema, CompanyQuerySchema
from app.utils.decorators import login_required
from datetime import datetime
from loguru import logger
from webargs.flaskparser import use_kwargs

# 创建Blueprint
company_bp = Blueprint("company", __name__)

@company_bp.route("/create_company", methods=["POST"])
@login_required
def create_company():
    """
    创建公司接口
    ---
    post:
      tags:
        - 公司管理
      summary: 创建新公司
      description: 创建一个新公司，并返回公司ID。
      requestBody:
        required: true
        content:
          application/json:
            schema: CompanyCreateSchema
      responses:
        200:
          description: 公司创建成功
        400:
          description: 参数验证失败
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 验证输入参数
        data = request.json
        schema = CompanyCreateSchema()
        validated_data = schema.load(data)

        # 创建新公司
        new_company = Company(
            compcode=validated_data["compcode"],
            compname=validated_data["compname"],
            compadd=validated_data.get("compadd"),
            uscicode=validated_data.get("uscicode"),
            createuser=session["empid"],  # 使用当前登录用户ID
            createdate=datetime.now(),
            status=0
        )
        db.add(new_company)
        db.commit()

        logger.info(f"公司 {validated_data['compname']} 创建成功")
        return jsonify({
            "message": "公司创建成功",
            "company_id": new_company.compid
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"公司创建失败: {e}")
        return jsonify({"error": "公司创建失败", "details": str(e)}), 500
    finally:
        db.close()

@company_bp.route("/edit_company/<int:company_id>", methods=["POST"])
@login_required
def edit_company(company_id):
    """
    修改公司信息接口
    ---
    post:
      tags:
        - 公司管理
      summary: 修改公司信息
      description: 修改指定公司的信息
      parameters:
        - name: company_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CompanyUpdateSchema
      responses:
        200:
          description: 公司信息修改成功
        400:
          description: 参数验证失败
        404:
          description: 公司不存在
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        # 验证输入参数
        data = request.json
        schema = CompanyUpdateSchema()
        validated_data = schema.load(data)

        # 查询要修改的公司
        company = db.query(Company).filter(Company.compid == company_id).first()
        if not company:
            return jsonify({"error": "公司不存在"}), 404

        # 更新公司信息
        if "compcode" in validated_data:
            company.compcode = validated_data["compcode"]
        if "compname" in validated_data:
            company.compname = validated_data["compname"]
        if "compadd" in validated_data:
            company.compadd = validated_data["compadd"]
        if "uscicode" in validated_data:
            company.uscicode = validated_data["uscicode"]
        if "status" in validated_data:
            company.status = validated_data["status"]
        
        # 更新修改人和修改时间
        company.modifyuser = session["empid"]
        company.modifydate = datetime.now()

        db.commit()

        logger.info(f"公司 {company_id} 信息修改成功")
        return jsonify({
            "message": "公司信息修改成功",
            "company_id": company_id
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"公司信息修改失败: {e}")
        return jsonify({"error": "公司信息修改失败", "details": str(e)}), 500
    finally:
        db.close()

@company_bp.route("/query_companies", methods=["POST"])
@login_required
@use_kwargs(CompanyQuerySchema)
def query_companies(**kwargs):
    """
    查询公司信息接口
    ---
    post:
      tags:
        - 公司管理
      summary: 查询公司信息
      description: 根据条件查询公司信息，支持模糊查询和时间范围查询
      requestBody:
        required: true
        content:
          application/json:
            schema: CompanyQuerySchema
      responses:
        200:
          description: 查询成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Company'
        500:
          description: 服务器内部错误
    """
    db = SessionLocal()
    try:
        query = db.query(Company)
        
        # 处理模糊查询条件
        if kwargs.get("compcode"):
            query = query.filter(Company.compcode.ilike(f"%{kwargs['compcode']}%"))
        if kwargs.get("compname"):
            query = query.filter(Company.compname.ilike(f"%{kwargs['compname']}%"))
        if kwargs.get("compadd"):
            query = query.filter(Company.compadd.ilike(f"%{kwargs['compadd']}%"))
            
        # 处理精确查询条件
        if kwargs.get("uscicode"):
            query = query.filter(Company.uscicode == kwargs["uscicode"])
        if kwargs.get("createuser"):
            query = query.filter(Company.createuser == kwargs["createuser"])
        if kwargs.get("status") is not None:
            query = query.filter(Company.status == kwargs["status"])
            
        # 处理时间范围查询
        if kwargs.get("createdate_start") and kwargs.get("createdate_end"):
            query = query.filter(
                Company.createdate.between(
                    kwargs["createdate_start"], kwargs["createdate_end"]
                )
            )
            
        companies = query.all()
        return jsonify([{
            "compid": company.compid,
            "compcode": company.compcode,
            "compname": company.compname,
            "compadd": company.compadd,
            "uscicode": company.uscicode,
            "createuser": company.createuser,
            "createdate": company.createdate.isoformat() if company.createdate else None,
            "status": company.status
        } for company in companies])
        
    except Exception as e:
        logger.error(f"查询公司信息失败: {e}")
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        db.close() 
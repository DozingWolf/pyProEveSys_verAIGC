from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.sql import func  # 导入 func 模块
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import Config

# 创建基类
Base = declarative_base()

# 创建数据库引擎和会话
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 用户表 (TMSTUSER)
class User(Base):
    __tablename__ = "TMSTUSER"
    empid = Column(Integer, primary_key=True, autoincrement=True)  # PK，用户内码
    empcode = Column(String(10), nullable=False)  # 用户工号
    empname = Column(String(15), nullable=False)  # 用户名
    passwd = Column(String(200), nullable=False)  # 密码密文（加盐加密后的密码）
    sex = Column(Integer, nullable=False, default=1)  # 性别，0男性，1女性
    mobile = Column(String(15)) # 中国手机号
    openid = Column(String(50)) # 微信openid
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 使用 func.now() 设置默认值
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用
    admin = Column(Integer, nullable=False, default=1)  # 管理员标记，0管理员，1普通用户

# 部门表 (TMSTDEPT)
class Department(Base):
    __tablename__ = "TMSTDEPT"
    deptid = Column(Integer, primary_key=True, autoincrement=True)  # PK，部门内码
    deptcode = Column(String(10), nullable=False)  # 部门编码
    deptname = Column(String(15), nullable=False)  # 部门名
    deptlocation = Column(String(30))  # 部门地址
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 公司表 (TMSTCOMP)
class Company(Base):
    __tablename__ = "TMSTCOMP"
    compid = Column(Integer, primary_key=True, autoincrement=True)  # PK，公司内码
    compcode = Column(String(10), nullable=False)  # 公司编码
    compname = Column(String(15), nullable=False)  # 公司名
    compadd = Column(String(30))  # 公司注册地址
    uscicode = Column(String(20))  # 统一社会信用代码
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 系统菜单表 (TMSTMENU)
class Menu(Base):
    __tablename__ = "TMSTMENU"
    menuid = Column(Integer, primary_key=True, autoincrement=True)  # PK，菜单id
    menucode = Column(String(10), nullable=False)  # 菜单编码
    mununame = Column(String(30), nullable=False)  # 菜单名
    subject = Column(String(5), nullable=False, default="MST")  # 分类
    level = Column(Integer, nullable=False)  # 菜单层级
    sortid = Column(Integer)  # 排序id
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 权限组表 (TAUTPERMISSIONGROUP)
class PermissionGroup(Base):
    __tablename__ = "TAUTPERMISSIONGROUP"
    pgroupid = Column(Integer, primary_key=True, autoincrement=True)  # PK,权限组id
    pgroupcode = Column(String(10), nullable=False)  # 权限组编码
    pgroupname = Column(String(15), nullable=False)  # 权限组名
    desc = Column(String(50))  # 权限组简要说明
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 权限组菜单表 (TAUTGROUPMENU)
class GroupMenu(Base):
    __tablename__ = "TAUTGROUPMENU"
    pgroupid = Column(Integer, primary_key=True, nullable=False)  # PK
    menuid = Column(Integer, primary_key=True, nullable=False)  # PK
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 用户权限组表 (TAUTUSERPERMISSION)
class UserPermission(Base):
    __tablename__ = "TAUTUSERPERMISSION"
    empid = Column(Integer, primary_key=True, nullable=False)  # PK，用户内码
    pgroupid = Column(Integer, primary_key=True, nullable=False)  # PK,权限组id
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 项目表 (TBUSPROJECT)
class Project(Base):
    __tablename__ = "TBUSPROJECT"
    prjid = Column(Integer, primary_key=True, autoincrement=True)  # PK,项目id
    prjcode = Column(String(20), nullable=False)  # 项目编码
    prjname = Column(String(50), nullable=False)  # 项目名
    cstid = Column(Integer)  # 客户id
    ownerid = Column(Integer, nullable=False)  # 项目经理
    sponsorid = Column(Integer, nullable=False)  # 项目发起人
    desc = Column(String(2000))  # 项目说明
    goal = Column(String(1000))  # 项目目标说明
    approvetime = Column(Date, server_default=func.now())  # 项目批准/发起时间
    expectedtime = Column(Date)  # 预期结束时间
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 事件表 (TBUSEVENT)
class Event(Base):
    __tablename__ = "TBUSEVENT"
    eventid = Column(Integer, primary_key=True, autoincrement=True)  # PK,事件id
    reporter = Column(Integer, nullable=False)  # 事件报告人id
    reportertime = Column(Date, nullable=False, server_default=func.now())  # 事件报告时间
    event = Column(String(2000), nullable=False) # 事件内容
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 项目关联事件表 (TBUSPRJEVENT)
class ProjectEvent(Base):
    __tablename__ = "TBUSPRJEVENT"
    prjid = Column(Integer, nullable=False)  # 项目id
    eventid = Column(Integer, nullable=False)  # 事件id
    leafid = Column(Integer, primary_key=True, nullable=False)  # PK，子叶id
    depth = Column(Integer, nullable=False)  # 深度数
    parentid = Column(Integer, nullable=False)  # 父节点id
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用

# 项目参与者表 (TBUSPRJMEMBER)
class ProjectMember(Base):
    __tablename__ = "TBUSPRJMEMBER"
    prjid = Column(Integer, primary_key=True, nullable=False)  # PK，项目id
    empid = Column(Integer, primary_key=True, nullable=False)  # PK，员工id
    createuser = Column(Integer, nullable=False)  # 创建人内码
    createdate = Column(Date, nullable=False, server_default=func.now())  # 创建时间
    modifyuser = Column(Integer)  # 修改人内码
    modifydate = Column(Date)  # 修改时间
    status = Column(Integer, nullable=False, default=0)  # 状态位，0正常，1停用
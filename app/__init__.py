from flask import Flask
from app.config import Config  # 导入配置

from flask_apispec import FlaskApiSpec  # 引入 Flask-APISpec
from apispec import APISpec  # 引入 APISpec
from apispec.ext.marshmallow import MarshmallowPlugin  # 引入 MarshmallowPlugin
from loguru import logger
from .config import Config

# 初始化Flask应用
app = Flask(__name__, static_folder="../frontend", static_url_path="/static")
app.config.from_object(Config)
# 加载配置
app.config.from_object(Config)

# 配置 Swagger
app.config.update({
    "APISPEC_SPEC": APISpec(
        title=Config.APISPEC_TITLE,
        version=Config.APISPEC_VERSION,
        openapi_version=Config.APISPEC_OPENAPI_VERSION,
        plugins=[MarshmallowPlugin()],
    ),
    "APISPEC_SWAGGER_URL": Config.APISPEC_SWAGGER_URL,
    "APISPEC_SWAGGER_UI_URL": Config.APISPEC_SWAGGER_UI_URL,
})
app.secret_key = Config.SECRET_KEY if hasattr(Config, 'SECRET_KEY') else "default_secret_key"


# 配置日志
logger.add(Config.LOG_FILE, level=Config.LOG_LEVEL, rotation="10 MB", retention="10 days")
logger.add(lambda msg: print(msg), level=Config.LOG_LEVEL)

# 初始化数据库
from .models import Base, engine

# 初始化数据库表
Base.metadata.create_all(bind=engine)

# 初始化 FlaskApiSpec
docs = FlaskApiSpec(app)

# 注册Blueprint
from .api.v1.user_api import user_bp
#from .api.v1.event_api import event_bp
from .api.v1.auth_api import auth_bp
from .api.v1.init_api import init_bp  # 导入初始化接口
#from .api.v1.test_crypto import test_crypto_bp  # 导入测试接口
from .api.v1.project_api import project_bp  # 导入项目管理接口
from .api.v1.event_api import event_bp  # 导入事件管理接口
from .api.v1.company_api import company_bp
from .api.v1.project_event_api import project_event_bp

app.register_blueprint(user_bp, url_prefix="/api/v1.0/MST")
#app.register_blueprint(event_bp, url_prefix="/prjeventsys/v1")
app.register_blueprint(auth_bp, url_prefix="/prjeventsys/v1")
app.register_blueprint(init_bp, url_prefix="/prjeventsys/v1")  # 注册初始化接口

#app.register_blueprint(test_crypto_bp, url_prefix='/api/v1') # 注册测试接口蓝图
app.register_blueprint(event_bp, url_prefix="/api/v1.0/BUS")  # 注册事件管理接口
app.register_blueprint(project_bp, url_prefix="/api/v1.0/BUS")  # 注册项目管理接口
app.register_blueprint(company_bp, url_prefix="/api/v1.0/MST")  # 注册公司管理接口
app.register_blueprint(project_event_bp, url_prefix="/api/v1.0/BUS")  # 注册项目事件管理接口

# 注册API文档
from .api.v1.user_api import user_routes
from .api.v1.auth_api import auth_routes
from .api.v1.project_api import project_routes
from .api.v1.event_api import event_routes
from .api.v1.company_api import company_routes
from .api.v1.project_event_api import project_event_routes

# 注册用户相关API文档
for route,path in user_routes:
    docs.register(route, endpoint=path, blueprint='user')

# # 注册认证相关API文档
for route,path in auth_routes:
    docs.register(route, endpoint=path,blueprint='auth')

# # 注册项目相关API文档
for route,path in project_routes:
    docs.register(route, endpoint=path, blueprint='project')

# # 注册事件相关API文档
for route,path in event_routes:
    docs.register(route, endpoint=path, blueprint='event')

# # 注册公司相关API文档
for route,path in company_routes:
    docs.register(route, endpoint=path, blueprint='company')

# # 注册项目事件相关API文档
for route,path in project_event_routes:
    docs.register(route, endpoint=path, blueprint='project_event')

import os
import configparser
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent  # 指向 app 目录的上一级（项目根目录）

# 读取 conf.ini 文件
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf.ini'))

class Config:
    # Flask配置
    FLASK_HOST = config.get('flask', 'host')
    FLASK_PORT = config.getint('flask', 'port')
    FLASK_DEBUG = config.getboolean('flask', 'debug')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = config.get('database', 'url')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 日志配置
    LOG_LEVEL = config.get('logging', 'level')
    LOG_FILE = os.path.join(BASE_DIR, config.get('logging', 'file'))

    # RSA配置
    RSA_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, config.get('rsa', 'private_key'))
    RSA_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, config.get('rsa', 'public_key'))

    @staticmethod
    def load_rsa_keys():
        with open(Config.RSA_PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()
        with open(Config.RSA_PUBLIC_KEY_PATH, 'r') as f:
            public_key = f.read()
        return private_key, public_key

    # AES配置
    AES_KEY = config.get('aes', 'key')

    # Flask-APISpec 配置项
    APISPEC_TITLE = "PrjEventSys API"
    APISPEC_VERSION = "1.0.0"
    APISPEC_OPENAPI_VERSION = "3.0.3"
    APISPEC_SWAGGER_URL = "/swagger/"  # Swagger UI 访问路径
    APISPEC_SWAGGER_UI_URL = "/swagger-ui/"  # Swagger UI 资源路径

    # BSER_DIR赋值
    BASE_DIR = BASE_DIR

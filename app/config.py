import os
import configparser
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 读取 conf.ini 文件
print(BASE_DIR)
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
    RSA_PRIVATE_KEY = config.get('rsa', 'private_key')
    RSA_PUBLIC_KEY = config.get('rsa', 'public_key')

    # AES配置
    AES_KEY = config.get('aes', 'key')
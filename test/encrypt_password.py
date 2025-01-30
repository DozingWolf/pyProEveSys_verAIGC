import sys
import os
import configparser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import argparse
import pyperclip
# 读取 conf.ini 文件中的 RSA 密钥
config = configparser.ConfigParser()
config.read('../conf.ini')
private_key = config.get('rsa', 'private_key')
public_key = config.get('rsa', 'public_key')

def encrypt_password(plaintext):
    """
    使用 RSA 公钥加密模拟前端将明文密码加密的效果
    :param plaintext: 明文密码
    :return: 加密后的密码字符串
    """
    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted = cipher.encrypt(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(f"RSA encryption failed: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt a password using RSA encryption.")
    parser.add_argument('-p', '--password', type=str, required=True, help='The password to encrypt')
    args = parser.parse_args()

    encrypted_password = encrypt_password(args.password)
    if encrypted_password:
        print(f"Encrypted password: {encrypted_password}")
        pyperclip.copy(encrypted_password)
        print("Encrypted password copied to clipboard.")

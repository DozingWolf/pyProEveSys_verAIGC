from flask import Blueprint, jsonify
from app.utils.crypto import PasswordService
from app.config import Config
from loguru import logger

# 创建Blueprint
test_crypto_bp = Blueprint("test_crypto", __name__)

@test_crypto_bp.route("/testcrypto", methods=["GET"])
def test_crypto():
    """
    测试 RSA 加密解密接口
    ---
    get:
      tags:
        - 测试接口
      summary: 测试 RSA 加密解密功能
      description: 对固定字符串"hello world"进行RSA加密解密测试，并记录每一步日志
      responses:
        200:
          description: 测试成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  original_text:
                    type: string
                    example: "hello world"
                  encrypted_text:
                    type: string
                  decrypted_text:
                    type: string
        500:
          description: 测试失败

    Returns:
        dict: 包含原始文本、加密后文本和解密后文本的字典
    """
    try:
        logger.info("开始 RSA 加密解密测试")
        
        # 定义测试字符串
        plaintext = "hello world"
        logger.info(f"原始明文: {plaintext}")
        
        # 加密过程
        logger.info("正在进行 RSA 加密...")
        PRIVATE_KEY , PUBLIC_KEY = Config.load_rsa_keys()
        # config['rsa']['private_key']
        public_key_path = PUBLIC_KEY
        # '../app/secure/public_key.pem'
        encrypted_text = PasswordService.encrypt_rsa(plaintext, public_key_path)
        logger.info(f"加密后的密文: {encrypted_text}")
        
        # 解密过程
        logger.info("正在进行 RSA 解密...")
        private_key_path = '../app/secure/private_key.pem'
        decrypted_text = PasswordService.decrypt_rsa(encrypted_text, private_key_path)
        logger.info(f"解密后的明文: {decrypted_text}")
        
        # 验证结果
        if plaintext == decrypted_text:
            logger.success("RSA 加密解密测试成功")
            return jsonify({
                "original_text": plaintext,
                "encrypted_text": encrypted_text,
                "decrypted_text": decrypted_text
            })
        else:
            logger.error("RSA 加密解密测试失败")
            return jsonify({"error": "Decryption result does not match original text"}), 500
            
    except Exception as e:
        logger.error(f"RSA 测试接口出现错误: {str(e)}")
        return jsonify({"error": f"Test failed: {str(e)}"}), 500

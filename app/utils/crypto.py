from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP ,PKCS1_v1_5
from Crypto.Hash import SHA256
import base64
import traceback
from loguru import logger
from .errors import BusinessError

class PasswordService:
    """
    密码服务类
    """

    @staticmethod
    def hash_password(password):
        """
        使用 werkzeug.security 对密码进行加盐加密
        """
        if not password:
            raise BusinessError(
                code=1001,
                module="PasswordService",
                input_data={"password": password},
                message="Password cannot be empty"
            )
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        """
        使用 werkzeug.security 校验密码是否正确
        """
        try:
            return check_password_hash(hashed_password, password)
        except Exception as e:
            raise BusinessError(
                code=1002,
                module="PasswordService",
                input_data={"password": password, "hashed_password": hashed_password},
                message=f"Password verification failed: {str(e)}"
            )

    @staticmethod
    def generate_rsa_key_pair():
        """
        生成 RSA 密钥对
        """
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    @staticmethod
    def encrypt_rsa(plaintext, public_key):
        """
        使用 RSA 公钥加密

        :param plaintext: 待加密的明文字符串
        :param public_key: RSA 公钥字符串
        :return: 加密后的 Base64 编码字符串
        """
        try:
            logger.debug(f"Loaded public key: {public_key}")  # 调试日志
            logger.debug(f"Loaded private key: {public_key}")  # 调试日志
            key = RSA.import_key(public_key)
            cipher = PKCS1_OAEP.new(key,hashAlgo=SHA256)
            encrypted = cipher.encrypt(plaintext.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            raise BusinessError(
                code=1003,
                module="PasswordService",
                input_data={"plaintext": plaintext, "public_key": public_key},
                message=f"RSA encryption failed: {str(e)}"
            )

    @staticmethod
    def decrypt_rsa(ciphertext, private_key):
        """
        使用 RSA 私钥解密

        :param ciphertext: 待解密的 Base64 编码字符串
        :param private_key: RSA 私钥字符串
        :return: 解密后的明文字符串
        """
        try:
            logger.debug(f"Loaded private key: {private_key}")  # 调试日志
            logger.debug(f"Loaded private key: {private_key}")  # 调试日志
            key = RSA.import_key(private_key)
            cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)  # 指定哈希算法为 SHA-256

            # 对 Base64 密文进行解码
            decoded_ciphertext = base64.b64decode(ciphertext)
            logger.debug(f'pain base64 ciphertext is: {decoded_ciphertext}') # 记录base64解码后的密文
            logger.debug(f"Decoded ciphertext length: {len(decoded_ciphertext)}")  # 记录密文长度
            logger.debug(f"Decoded ciphertext (Hex): {decoded_ciphertext.hex()}")  # 记录解码后的十六进制表示

            if len(decoded_ciphertext) != 256:  # 检查密文长度
                logger.debug("Ciphertext length is incorrect")

            # 解密
            decrypted = cipher.decrypt(decoded_ciphertext)
            logger.debug(f"Decrypted text: {decrypted.decode('utf-8')}")
            return decrypted.decode('utf-8')
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"Decryption error details: {str(e)}\nTraceback:\n{error_traceback}")
            raise BusinessError(
                code=1004,
                module="PasswordService",
                input_data={
                    "ciphertext": ciphertext,
                    "private_key": private_key,
                    "decoded_ciphertext": base64.b64decode(ciphertext).hex()  # 记录解码后的十六进制表示
                },
                message=f"RSA decryption failed: {str(e)}"
            )

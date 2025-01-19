from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
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
        """
        try:
            key = RSA.import_key(public_key)
            cipher = PKCS1_OAEP.new(key)
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
        """
        try:
            key = RSA.import_key(private_key)
            cipher = PKCS1_OAEP.new(key)
            decrypted = cipher.decrypt(base64.b64decode(ciphertext))
            return decrypted.decode('utf-8')
        except Exception as e:
            raise BusinessError(
                code=1004,
                module="PasswordService",
                input_data={"ciphertext": ciphertext, "private_key": private_key},
                message=f"RSA decryption failed: {str(e)}"
            )
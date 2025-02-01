// 刷新验证码
function refreshCaptcha() {
    const captchaImage = document.getElementById('captchaImage');
    captchaImage.src = '/prjeventsys/v1/captcha?' + new Date().getTime(); // 添加时间戳防止缓存
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const empcode = document.getElementById('empcode').value;
        const password = document.getElementById('password').value;
        const captcha = document.getElementById('captcha').value;
        console.log('plain password text is:',password)
        try {
            // 检查密码长度
            if (password.length > 214) {
                throw new Error('密码过长，无法加密');
            }

            // 加载本地公钥文件
            console.log('Loading public key...');
            const publicKeyResponse = await fetch('/static/secure/public_key.pem');
            if (!publicKeyResponse.ok) {
                throw new Error(`Failed to load public key: HTTP error! status: ${publicKeyResponse.status}`);
            }
            const publicKeyPem = await publicKeyResponse.text();
            console.log('Public key loaded:', publicKeyPem);

            // 导入公钥
            const publicKey = await window.crypto.subtle.importKey(
                'spki',
                await base64ToArrayBuffer(publicKeyPem),
                {
                    name: 'RSA-OAEP',
                    hash: { name: 'SHA-256' } // 指定哈希算法
                },
                false,
                ['encrypt']
            );
            console.log('Public key imported successfully.');

            // 将密码转换为UTF-8编码的字节数组
            const passwordBuffer = new TextEncoder().encode(password);
            console.log('Password buffer:', passwordBuffer);

            // 加密密码
            const encryptedData = await window.crypto.subtle.encrypt(
                {
                    name: 'RSA-OAEP',
                    hash: { name: 'SHA-256' } // 指定哈希算法
                },
                publicKey,
                passwordBuffer
            );
            console.log('Encrypted data length:', encryptedData.byteLength);  // 打印加密数据长度
            console.log('Encrypted data:', encryptedData);

            // 将加密后的数据转换为Base64字符串
            const encryptedPassword = arrayBufferToBase64(encryptedData);
            console.log('Encrypted password (Base64):', encryptedPassword);

            // 发送登录请求
            console.log('Sending login request...');
            const response = await fetch('/prjeventsys/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ empcode, password: encryptedPassword, captcha })
            });
            console.log('Response status:', response.status);
            const result = await response.json();
            console.log('Response content:', result);

            if (result.message) {
                alert(result.message || '登录成功');
                window.location.href = '/'; // 跳转到首页
            } else {
                document.getElementById('errorMessage').textContent = result.error || '登录失败';
            }
        } catch (error) {
            console.error('Unexpected error:', error);
            console.error('Error stack:', error.stack); // 打印错误堆栈
            document.getElementById('errorMessage').textContent = error.message || '发生未知错误，请稍后再试';
        }
    });
});

// 页面加载时刷新验证码
window.onload = function() {
    refreshCaptcha();
};

// 将Base64字符串转换为ArrayBuffer
async function base64ToArrayBuffer(base64) {
    // 去掉PEM文件的头部和尾部
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    base64 = base64
        .replace(pemHeader, '')
        .replace(pemFooter, '')
        .replace(/\s+/g, ''); // 去掉所有空白字符

    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

// 将ArrayBuffer转换为Base64字符串
function arrayBufferToBase64(buffer) {
    const byteArray = new Uint8Array(buffer);
    return btoa(String.fromCharCode.apply(null, byteArray));
}
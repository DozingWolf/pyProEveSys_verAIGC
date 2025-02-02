// 简易登录逻辑
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('simpleLoginForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const empcode = document.getElementById('empcode').value;
        const captcha = document.getElementById('captcha').value;
        const password = document.getElementById('password').value;

        try {
            // 发送登录请求
            console.log('Sending simple login request...');
            const response = await fetch('/prjeventsys/v1/simple_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ empcode, captcha, password })
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

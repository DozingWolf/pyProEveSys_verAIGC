import requests

# 测试初始化管理员用户接口
def test_init_admin():
    url = "http://127.0.0.1:6231/prjeventsys/v1/init_admin"
    response = requests.post(url)
    if response.status_code == 200:
        print("Test passed: Admin user created successfully")
        print("Response:", response.json())
    else:
        print("Test failed: Failed to create admin user")
        print("Response:", response.json())

if __name__ == "__main__":
    test_init_admin()
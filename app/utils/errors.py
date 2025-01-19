class BusinessError(Exception):
    """
    自定义业务错误类
    """
    def __init__(self, code, module, input_data, message):
        self.code = code  # 错误代码（4 位数字）
        self.module = module  # 出现错误的模块名
        self.input_data = input_data  # 出现错误时的入参
        self.message = message  # 具体错误内容

    def __str__(self):
        return f"BusinessError(code={self.code}, module={self.module}, input_data={self.input_data}, message={self.message})"
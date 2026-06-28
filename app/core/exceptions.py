"""
业务异常定义 —— 按异常类型映射 HTTP 状态码，避免全局 500
"""


class AppException(Exception):
    """业务异常基类 —— 实例化时可用自定义消息覆盖类级别 message"""

    status_code: int = 500
    message: str = "系统内部错误"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(message or self.message)


class ValidationException(AppException):
    """请求参数校验失败"""
    status_code = 400
    message = "请求参数不合法"


class FileProcessingException(AppException):
    """文件处理失败（格式不支持 / 损坏）"""
    status_code = 400
    message = "文件处理失败"


class LLMServiceException(AppException):
    """LLM 调用失败"""
    status_code = 502
    message = "AI 服务暂不可用，请稍后重试"


class NotFoundException(AppException):
    """资源不存在"""
    status_code = 404
    message = "请求的资源不存在"

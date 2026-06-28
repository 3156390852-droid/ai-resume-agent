"""
业务异常类测试
"""
import pytest
from app.core.exceptions import (
    AppException,
    ValidationException,
    FileProcessingException,
    LLMServiceException,
    NotFoundException,
)


class TestExceptions:
    """异常层次结构测试"""

    def test_all_subclass_of_app(self):
        """所有业务异常都是 AppException 子类"""
        assert issubclass(ValidationException, AppException)
        assert issubclass(FileProcessingException, AppException)
        assert issubclass(LLMServiceException, AppException)
        assert issubclass(NotFoundException, AppException)

    def test_status_codes(self):
        """各异常有正确的 HTTP 状态码"""
        assert ValidationException.status_code == 400
        assert FileProcessingException.status_code == 400
        assert NotFoundException.status_code == 404
        assert LLMServiceException.status_code == 502
        assert AppException.status_code == 500

    def test_custom_message(self):
        """实例化消息覆盖类级别默认值"""
        exc = ValidationException("缺少必填字段 name")
        assert exc.message == "缺少必填字段 name"  # 实例消息覆盖类默认
        assert str(exc) == "缺少必填字段 name"

    def test_catch_as_base(self):
        """可以用 AppException 统一捕获"""
        try:
            raise FileProcessingException("文件损坏")
        except AppException as e:
            assert e.status_code == 400

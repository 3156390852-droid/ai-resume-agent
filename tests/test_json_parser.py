"""
safe_json_loads 单元测试
"""
import pytest
from app.utils.json_parser import safe_json_loads


class TestSafeJsonLoads:
    """JSON 解析器测试"""

    def test_parse_valid_json(self):
        """正常 JSON"""
        result = safe_json_loads('{"name": "张三", "score": 90}')
        assert result == {"name": "张三", "score": 90}

    def test_parse_json_with_markdown_fence(self):
        """带 ```json 标记"""
        result = safe_json_loads('```json\n{"a": 1}\n```')
        assert result == {"a": 1}

    def test_parse_json_with_extra_text(self):
        """JSON 外有额外文字"""
        result = safe_json_loads('这是分析结果：\n{"result": "ok"}\n分析完毕。')
        assert result == {"result": "ok"}

    def test_parse_nested_json(self):
        """嵌套 JSON"""
        result = safe_json_loads('{"user": {"name": "李四", "skills": ["Python"]}}')
        assert result == {"user": {"name": "李四", "skills": ["Python"]}}

    def test_parse_array_json(self):
        """数组 JSON"""
        result = safe_json_loads('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_empty_string_raises(self):
        """空字符串抛异常"""
        with pytest.raises(ValueError, match="Empty"):
            safe_json_loads("")

    def test_no_json_found_raises(self):
        """无 JSON 内容抛异常"""
        with pytest.raises(ValueError, match="No JSON"):
            safe_json_loads("这是纯文本，没有任何 JSON")

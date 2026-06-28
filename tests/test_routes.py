"""
API 集成测试（不依赖真实 LLM / DB）
"""
import pytest
from unittest.mock import patch, MagicMock


class TestRootEndpoint:
    """根路径测试"""

    def test_root_health(self, client):
        """GET / 健康检查"""
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["message"] == "AI Resume Agent Running"


class TestUploadResume:
    """简历上传接口测试"""

    def test_upload_invalid_extension(self, client):
        """上传不支持的文件类型应返回 400"""
        resp = client.post(
            "/upload-resume",
            files={"file": ("test.txt", b"hello world", "text/plain")},
        )
        assert resp.status_code == 400
        assert "不支持" in resp.json()["message"]

    def test_upload_no_file(self, client):
        """不传文件应返回 422"""
        resp = client.post("/upload-resume")
        assert resp.status_code == 422

    @patch("app.api.routes.parse_resume")
    @patch("app.api.routes.extract_resume_info")
    def test_upload_pdf_success(self, mock_extract, mock_parse, client):
        """上传 PDF 成功路径"""
        mock_parse.return_value = "模拟简历文本"
        mock_extract.return_value = MagicMock(
            model_dump=lambda: {"name": "张三", "skills": ["Python"]}
        )

        resp = client.post(
            "/upload-resume",
            files={"file": ("resume.pdf", b"%PDF-1.4 mock", "application/pdf")},
        )
        assert resp.status_code == 200
        assert resp.json()["filename"] == "resume.pdf"
        assert "data" in resp.json()


class TestMatchEndpoint:
    """岗位匹配接口测试"""

    def test_match_empty_resume_text(self, client):
        """resume_text 为空应返回 400"""
        resp = client.post("/match", data={"resume_text": "", "jd_text": "需要Python"})
        assert resp.status_code == 400

    def test_match_empty_jd_text(self, client):
        """jd_text 为空应返回 400"""
        resp = client.post("/match", data={"resume_text": "我会Python", "jd_text": ""})
        assert resp.status_code == 400

    def test_match_missing_fields(self, client):
        """缺少必填字段——空字符串触发校验返回 400"""
        resp = client.post("/match", data={"resume_text": "test"})
        assert resp.status_code == 400

    def test_match_text_too_long(self, client):
        """超长文本应返回 400"""
        long_text = "x" * 10_001
        resp = client.post(
            "/match",
            data={"resume_text": "正常文本", "jd_text": long_text},
        )
        assert resp.status_code == 400


class TestHistoryEndpoint:
    """历史记录接口测试"""

    @patch("app.api.routes.get_records")
    def test_history_returns_list(self, mock_get, client):
        """GET /history 返回数组"""
        mock_get.return_value = []
        resp = client.get("/history")
        assert resp.status_code == 200
        assert resp.json() == []

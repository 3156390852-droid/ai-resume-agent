"""
pytest 共享夹具
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# 确保项目根目录在 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试时用临时 .env 覆盖真实配置
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_API_BASE", "https://test.api.com/v1")
os.environ.setdefault("MODEL_NAME", "test-model")
os.environ.setdefault("EMBEDDING_MODEL", "test-embedding")
os.environ.setdefault("MYSQL_URL", "mysql+pymysql://test:test@localhost:3306/test_db")


@pytest.fixture
def client():
    """FastAPI TestClient"""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_pdf_path():
    """测试用 PDF 文件路径"""
    return os.path.join(os.path.dirname(__file__), "..", "data", "test_resume.pdf")

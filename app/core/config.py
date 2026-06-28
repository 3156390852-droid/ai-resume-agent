"""
应用配置 —— 基于 Pydantic BaseSettings，启动时自动校验必填字段
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，从 .env 自动加载，启动即校验"""

    # ── LLM 配置 ──
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str
    MODEL_NAME: str
    EMBEDDING_MODEL: str

    # ── 数据库 ──
    MYSQL_URL: str

    # ── 服务配置（有默认值） ──
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    MAX_UPLOAD_SIZE_MB: int = 10
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()

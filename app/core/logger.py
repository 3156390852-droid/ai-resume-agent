"""
日志配置 —— 同时输出到文件和控制台（Docker 可见）
"""
import logging
import sys
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("resume_agent")
logger.setLevel(logging.INFO)

# ── 格式 ──
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# ── 文件输出 ──
file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ── 控制台输出（Docker / 开发调试可见） ──
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

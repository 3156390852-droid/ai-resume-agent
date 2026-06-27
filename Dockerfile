# ============================================
# AI Resume Agent — Docker 镜像
# 基于 Python 3.11，FastAPI + LangChain + FAISS
# ============================================

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（MySQL 客户端库 + 中文字体）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    fonts-wqy-microhei \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建数据与日志目录
RUN mkdir -p /app/data /app/logs

# 暴露 FastAPI 端口
EXPOSE 8000

# 启动服务
CMD ["python", "run.py"]

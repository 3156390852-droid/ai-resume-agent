# 🧠 AI Resume Agent

> 基于大语言模型的智能简历解析与岗位匹配分析系统 —— 面向上海/苏州 AI 应用工程师岗位优化

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.3-1c3c3c.svg)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-✔-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 项目简介

AI Resume Agent 是一个智能简历分析系统，能够：

- 自动解析 **PDF / Word** 格式的简历文件
- 利用 **LLM（大语言模型）** 提取结构化信息（含期望职位、城市、薪资、GitHub 等）
- 结合 **RAG（检索增强生成）** 进行岗位匹配分析
- 输出匹配评分、技能缺口分析及个性化学习建议
- 生成 **BOSS 直聘招呼语模板** 与面试准备建议
- 给出 **投递决策**（是否建议投递该岗位）

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 📄 简历解析 | 支持 PDF 和 Word 格式，自动提取纯文本 |
| 🧠 结构化提取 | LLM 提取姓名、技能、教育经历、项目经验、期望城市/薪资、GitHub |
| 🎯 岗位匹配 | 简历与 JD 语义匹配，输出 0-100 评分 |
| 🔍 技能缺口 | 识别匹配与缺失技能，生成学习路线 |
| 📚 学习建议 | 结合岗位知识库，给出个性化提升方案 |
| 💬 招呼语生成 | 针对岗位自动生成 BOSS 直聘个性化招呼语模板 |
| 🎤 面试建议 | 输出针对该岗位的面试准备要点 |
| ✅ 投递决策 | 综合匹配度给出是否建议投递的判断 |
| 💾 历史记录 | MySQL 持久化存储所有分析结果 |

---

## 🧱 技术栈

| 层级 | 技术 |
|------|------|
| **Web 框架** | FastAPI + Uvicorn |
| **LLM 框架** | LangChain + LangGraph |
| **模型服务** | DeepSeek-V3（硅基流动 SiliconFlow API） |
| **数据校验** | Pydantic v2 |
| **RAG** | 自建向量知识库（65 条行业知识）+ FAISS 向量检索 |
| **Embedding** | BGE-M3（硅基流动 API） |
| **数据库** | MySQL + SQLAlchemy ORM |
| **文档解析** | PyPDF2 / python-docx |

---

## 📁 项目结构

```
resume-agent/
├── app/
│   ├── api/
│   │   └── routes.py            # API 路由定义
│   ├── core/
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   └── logger.py            # 日志模块
│   ├── models/
│   │   ├── resume_schema.py     # 简历结构化模型（含期望职位/城市/薪资/GitHub）
│   │   ├── match_schema.py      # 匹配结果模型（含招呼语/面试建议/投递决策）
│   │   └── resume_record.py     # 数据库 ORM 模型
│   ├── rag/
│   │   ├── knowledge_base.py    # 知识库（65条：AI技术栈 + 上海/苏州市场 + BOSS直聘策略）
│   │   └── vector_store.py      # FAISS 向量存储与检索
│   ├── services/
│   │   ├── llm_extractor.py     # LLM 简历信息提取
│   │   ├── job_matcher.py       # 岗位匹配 + 招呼语生成
│   │   └── db_service.py        # 数据库 CRUD
│   ├── utils/
│   │   ├── parser.py            # PDF/Word 解析
│   │   └── json_parser.py       # JSON 格式处理
│   └── main.py                  # FastAPI 应用入口
├── data/                        # 简历文件存储
├── logs/                        # 日志文件
├── tests/                       # 测试用例
├── requirements.txt             # 依赖列表
├── run.py                       # 启动脚本
├── create_db.py                 # 数据库初始化
└── .env                         # 环境变量配置
```

---

## 🏗️ 系统架构

```
用户上传简历 (PDF/Word)
        ↓
FastAPI 接收请求  ──→  保存文件至 /data
        ↓
解析器提取纯文本 (parser.py)
        ↓
LLM 结构化提取 (LangChain + Pydantic)
  · 姓名  · 技能  · 教育经历  · 项目经验  · 期望城市/薪资  · GitHub
        ↓
向量知识库检索 (FAISS + 65条行业知识)
        ↓
LLM 岗位匹配分析
  · 匹配评分  · 已匹配/缺失技能  · 学习建议  · 招呼语模板  · 面试建议  · 投递决策
        ↓
MySQL 持久化存储
        ↓
返回 JSON 分析结果
```

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.11+
- MySQL 8.0+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

编辑 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key          # 硅基流动 API Key
OPENAI_API_BASE=https://api.siliconflow.cn/v1
MODEL_NAME=deepseek-ai/DeepSeek-V3
EMBEDDING_MODEL=BAAI/bge-m3
MYSQL_URL=mysql+pymysql://user:password@localhost:3306/ai_resume
```

### 4. 初始化数据库

```bash
python create_db.py
```

### 5. 启动服务

```bash
python run.py
```

服务启动后访问：**http://localhost:8000**

---

## 🐳 Docker 部署（推荐）

无需手动安装 Python 和 MySQL，一键启动全部服务。

### 1. 准备环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

### 2. 构建并启动

```bash
docker-compose up -d
```

首次启动会自动：
- 拉取 `python:3.11-slim` 基础镜像 + 安装中文字体
- 拉取 `mysql:8.0` 镜像
- `pip install` 所有依赖
- 自动创建 `ai_resume` 数据库

### 3. 初始化数据库表

```bash
docker exec -it resume-app python create_db.py
```

### 4. 访问服务

打开浏览器访问：**http://localhost:8000**

### 常用命令

| 命令 | 说明 |
|------|------|
| `docker-compose up -d` | 后台启动 |
| `docker-compose down` | 停止服务 |
| `docker-compose logs -f app` | 查看应用日志 |
| `docker-compose build --no-cache` | 重新构建镜像 |

---

## 📡 API 接口

### 根路径

```
GET /
```

返回服务运行状态。

---

### 上传简历 & 结构化解析

```
POST /upload-resume
Content-Type: multipart/form-data

参数:
  file: PDF 或 Word 文件

返回:
{
  "filename": "简历.pdf",
  "data": {
    "name": "张三",
    "desired_position": "AI应用工程师",
    "location": "上海",
    "salary_expectation": "8-13K",
    "summary": "计算机专业本科生，擅长LLM应用开发...",
    "skills": ["Python", "FastAPI", "LangChain", "RAG", "MySQL"],
    "education": ["南京航空航天大学 计算机科学与技术 本科 2023-2027"],
    "experience": ["独立开发AI简历解析系统..."],
    "projects": [
      {
        "name": "AI Resume Agent",
        "date": "2026.02-2026.06",
        "stack": ["FastAPI", "LangChain", "DeepSeek-V3"],
        "highlights": ["实现PDF/Word自动解析", "RAG匹配评分0-100"]
      }
    ],
    "certifications": ["CET-6", "校级奖学金"],
    "github": "https://github.com/xxx"
  }
}
```

---

### 简历 + JD 匹配分析

```
POST /match
Content-Type: application/x-www-form-urlencoded

参数:
  resume_text: 简历纯文本内容
  jd_text:     岗位 JD 文本内容

返回:
{
  "match_score": 85,
  "matched_skills": ["Python", "FastAPI", "MySQL"],
  "missing_skills": ["Docker", "FAISS"],
  "reason": "候选人的Python和FastAPI技术栈与岗位高度匹配...",
  "suggestions": ["学习FAISS向量检索基础（1-2天可上手）", "将Docker应用于项目部署"],
  "greeting_template": "您好！我是南航计算机本科生，熟练掌握LangChain+RAG+FastAPI，独立开发过AI简历解析系统，希望能和您深入聊聊这个岗位！",
  "interview_tips": ["准备介绍RAG系统的技术选型理由", "复习FastAPI异步编程原理"],
  "should_apply": true
}
```

---

### 查看历史记录

```
GET /history

返回所有历史匹配记录（含 ID、文件名、匹配结果）
```

---

## 🧠 项目亮点

- ✨ **Pydantic 结构化输出** — 保证 LLM 返回的 JSON 格式稳定可靠
- 🔧 **模块化设计** — Parser / LLM / Matcher / DB 职责清晰，易于扩展
- 📚 **RAG 增强匹配** — 65 条行业知识覆盖 AI 技术栈 + 上海/苏州市场 + BOSS 直聘策略
- 💬 **智能招呼语** — 针对岗位自动生成个性化 BOSS 直聘招呼语，突出匹配技能
- 🎯 **投递决策支持** — 综合匹配度给出是否建议投递的判断，避免盲目海投
- 🛡️ **全局异常处理** — 统一的异常拦截与日志记录
- 📝 **工程化日志** — 关键步骤均有日志追踪，方便排查问题

---

## 📝 License

MIT © 2025

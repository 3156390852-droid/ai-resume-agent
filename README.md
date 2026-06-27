# AI Resume Agent（智能简历分析与岗位匹配系统）

## 项目简介

本项目是一个基于大语言模型（LLM）的智能简历分析系统，能够自动解析用户简历，并与岗位JD进行语义匹配分析，输出匹配评分、技能缺口及学习建议。

---

## 核心功能

- 支持 PDF / Word 简历解析
- LLM自动提取结构化信息（姓名 / 技能 / 经历 / 教育）
- 简历与岗位JD语义匹配分析
- 输出匹配评分（0-100）
- 技能缺口分析
- 个性化学习路径推荐
- MySQL记录历史分析结果

---

##  技术栈

- FastAPI（后端接口）
- LangChain（LLM应用框架）
- DeepSeek（硅基流动API）
- Pydantic（结构化输出）
- MySQL（数据存储）
- PDF / Word解析

---

## 项目亮点

- 使用 Prompt Engineering 提升信息抽取准确性
- 使用 Pydantic 保证LLM输出结构稳定
- RAG增强岗位匹配语义理解能力
- 模块化设计（Parser / LLM / Matcher / DB）
- 工程化日志与异常处理

---

## 启动方式

```bash
pip install -r requirements.txt
python run.py
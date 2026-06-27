"""
LLM 简历结构化提取器

使用 LangChain + DeepSeek-V3 从简历纯文本中提取结构化信息，
输出符合 ResumeInfo 模型的 JSON 数据。
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.core.logger import logger
from app.models.resume_schema import ResumeInfo

load_dotenv(dotenv_path=".env")

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    model=os.getenv("MODEL_NAME").strip(),
    temperature=0
)

structured_llm = llm.with_structured_output(ResumeInfo)


def extract_resume_info(text: str) -> ResumeInfo:
    """从简历文本中提取结构化信息"""

    prompt = f"""你是一位资深招聘专家和简历分析师。请从以下简历文本中提取结构化信息。

注意：
1. 技能列表要尽可能全面，包括编程语言、框架、工具、平台、数据库、AI/LLM 相关技术
2. 项目经历要提取名称、时间、技术栈和关键成果
3. 教育经历保留学校全称、专业、学历、时间
4. 如果简历中未明确提及某个字段，返回空字符串或空列表

---

【简历文本】
{text}

---

请按照以下结构提取信息：
- name: 候选人姓名
- desired_position: 期望职位
- location: 期望城市
- salary_expectation: 期望薪资
- summary: 个人总结（2-3句话概括核心竞争力）
- skills: 技能列表（尽可能全面）
- education: 教育经历列表
- experience: 工作/项目经历文本描述列表
- projects: 结构化项目列表，每项含 name/date/stack/highlights
- certifications: 证书与语言能力列表
- github: GitHub 地址
- portfolio: 个人作品集/博客地址
"""

    try:
        logger.info("开始LLM简历结构化提取...")
        result = structured_llm.invoke(prompt)
        logger.info(f"LLM结构化成功，提取到 {len(result.skills)} 项技能")
        return result
    except Exception as e:
        logger.error(f"LLM调用失败: {str(e)}")
        raise e

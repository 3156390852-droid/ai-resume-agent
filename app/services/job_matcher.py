"""
岗位匹配服务

结合 RAG 向量知识库进行简历与 JD 的语义匹配分析，
输出匹配评分、技能对比、学习建议，以及 BOSS 直聘招呼语和投递策略。
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.rag.vector_store import retrieve_context
from app.models.match_schema import MatchResult
from app.core.logger import logger

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0
)

structured_llm = llm.with_structured_output(MatchResult)


def match_resume_and_job(resume: str, jd: str) -> MatchResult:
    """
    分析简历与 JD 的匹配程度

    Args:
        resume: 简历纯文本内容
        jd: 岗位 JD 文本内容

    Returns:
        MatchResult: 包含匹配评分、技能对比、学习建议、招呼语等
    """

    # RAG 检索相关知识
    context = retrieve_context(jd)
    context_text = "\n".join(f"· {item}" for item in context)

    prompt = f"""你是一位资深 HR 和技术面试官，专注于 AI/大模型应用开发领域的招聘。

请结合下方「行业知识库」，对这份简历和岗位 JD 进行全面分析。

---

【行业知识库（上海/苏州 AI 应用工程师市场）】
{context_text}

---

【候选人简历】
{resume}

---

【岗位 JD】
{jd}

---

请从以下维度输出分析结果：

## 1. 匹配评分（0-100）
- 90+：简历与 JD 高度匹配，强烈推荐投递
- 70-89：大部分技能匹配，建议投递
- 50-69：部分匹配，可作为备选
- 40以下：匹配度低，不建议投递

## 2. 技能对比
- matched_skills：简历中已有且 JD 要求的技能（仅列出明确匹配的）
- missing_skills：JD 要求但简历中缺失的技能（按重要性排序）

## 3. 匹配原因分析（reason）
用 2-3 句话分析：为什么匹配/不匹配，候选人的核心竞争力是什么

## 4. 学习建议（suggestions）
如果存在技能缺口，给出具体、可执行的学习建议（如"花 1-2 天学习 FAISS 向量检索基础"），按优先级排序

## 5. BOSS 直聘招呼语模板（greeting_template）
生成一句个性化招呼语，格式为：「核心身份 + 匹配的技能亮点 + 项目成果（数据量化） + 表达兴趣」
- 必须包含具体技能关键词（让 HR 一眼看到匹配点）
- 风格专业但不死板
- 控制在 80 字以内
- 示例：「您好！我是南航计算机本科生，熟练掌握 LangChain + RAG + FastAPI 技术栈，独立开发过 AI 简历解析系统，希望能和您深入聊聊这个岗位的机会！」

## 6. 面试准备建议（interview_tips）
列出 2-4 条针对该岗位的面试准备要点

## 7. 是否建议投递（should_apply）
匹配分数低于 40 分或岗位要求 3 年以上经验但候选人为应届生时，标记为 false
"""

    try:
        logger.info("开始岗位匹配分析...")
        result: MatchResult = structured_llm.invoke(prompt)
        logger.info(f"匹配分析完成，评分: {result.match_score}")
        return result
    except Exception as e:
        logger.error(f"匹配分析失败: {str(e)}")
        raise e

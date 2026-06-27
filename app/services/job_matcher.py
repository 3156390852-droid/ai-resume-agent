import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.rag.vector_store import retrieve_context
from app.models.match_schema import MatchResult

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0
)

structured_llm = llm.with_structured_output(MatchResult)


def match_resume_and_job(resume: str, jd: str):

    # 🧠 1. RAG检索知识
    context = retrieve_context(jd)

    context_text = "\n".join(context)

    prompt = f"""
你是资深HR和技术面试官，请结合“岗位知识库”进行分析。

---

【岗位知识库】
{context_text}

---

【简历】
{resume}

---

【岗位JD】
{jd}

---

请输出：
1. 匹配分数（0-100）
2. 已匹配技能
3. 缺失技能
4. 专业原因分析
5. 学习建议
"""

    result = structured_llm.invoke(prompt)

    return result
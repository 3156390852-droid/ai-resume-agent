
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
def extract_resume_info(text: str):
    try:
        logger.info("开始LLM简历结构化")

        result = structured_llm.invoke(text)

        logger.info("LLM结构化成功")
        return result

    except Exception as e:
        logger.error(f"LLM调用失败: {str(e)}")
        raise e
structured_llm = llm.with_structured_output(ResumeInfo)


def extract_resume_info(text: str) -> ResumeInfo:
    prompt = f"提取简历信息：\n{text}"
    return structured_llm.invoke(prompt)
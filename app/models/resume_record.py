from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class ResumeRecord(Base):
    """
    简历分析记录表
    """

    __tablename__ = "resume_records"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255))

    resume_text = Column(Text)

    resume_json = Column(Text)   # LLM结构化结果（JSON字符串）

    jd_text = Column(Text)

    match_result = Column(Text)  # 匹配结果JSON
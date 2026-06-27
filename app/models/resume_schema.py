from pydantic import BaseModel, Field
from typing import List


class ResumeInfo(BaseModel):
    """
    简历结构化信息
    """

    name: str = Field(
        default="",
        description="候选人姓名"
    )

    skills: List[str] = Field(
        default_factory=list,
        description="候选人技能列表"
    )

    education: List[str] = Field(
        default_factory=list,
        description="教育经历"
    )

    experience: List[str] = Field(
        default_factory=list,
        description="工作或项目经历"
    )
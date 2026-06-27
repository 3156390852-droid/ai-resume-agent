from pydantic import BaseModel, Field
from typing import List


class MatchResult(BaseModel):
    match_score: int = Field(description="岗位匹配分数 0-100")

    matched_skills: List[str] = Field(default_factory=list)

    missing_skills: List[str] = Field(default_factory=list)

    reason: str = Field(default="匹配原因分析")

    suggestions: List[str] = Field(default_factory=list)
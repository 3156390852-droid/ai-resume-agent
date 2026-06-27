"""
岗位匹配结果模型

基于简历与 JD 的语义匹配分析，输出匹配评分、技能对比、
学习建议，以及针对 BOSS 直聘的招呼语和投递策略建议。
"""

from pydantic import BaseModel, Field
from typing import List


class MatchResult(BaseModel):
    """简历与岗位 JD 匹配分析结果"""

    # ── 匹配评分 ──
    match_score: int = Field(
        description="岗位匹配分数 0-100。90+ 强烈推荐投递；70-89 匹配度较高；50-69 部分匹配可尝试；50以下不建议"
    )

    # ── 技能对比 ──
    matched_skills: List[str] = Field(
        default_factory=list,
        description="已匹配的技能列表（简历中有且 JD 要求的）"
    )

    missing_skills: List[str] = Field(
        default_factory=list,
        description="缺失技能列表（JD 要求但简历中未体现的）"
    )

    # ── 分析 ──
    reason: str = Field(
        default="",
        description="匹配原因分析，用 2-3 句话说明为什么匹配/不匹配，指出核心竞争力"
    )

    # ── 学习建议 ──
    suggestions: List[str] = Field(
        default_factory=list,
        description="个性化学习/提升建议，帮助弥合技能缺口，按优先级排序"
    )

    # ── 投递策略建议（新增） ──
    greeting_template: str = Field(
        default="",
        description="针对该岗位的个性化 BOSS 直聘招呼语模板，突出匹配技能和项目成果"
    )

    interview_tips: List[str] = Field(
        default_factory=list,
        description="针对该岗位的面试准备建议"
    )

    should_apply: bool = Field(
        default=True,
        description="是否建议投递该岗位（匹配分数低于 40 分或岗位要求明显不符时建议跳过）"
    )

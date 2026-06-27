from pydantic import BaseModel, Field
from typing import List, Optional


class ProjectExperience(BaseModel):
    """项目经历"""
    name: str = Field(default="", description="项目名称")
    date: str = Field(default="", description="项目时间，如 2026.02-2026.06")
    stack: List[str] = Field(default_factory=list, description="技术栈列表")
    highlights: List[str] = Field(default_factory=list, description="项目亮点/成果")


class ResumeInfo(BaseModel):
    """
    简历结构化信息 —— 面向 AI 应用工程师岗位优化
    """

    # ── 基本信息 ──
    name: str = Field(default="", description="候选人姓名")

    desired_position: str = Field(
        default="",
        description="期望职位，如 AI应用工程师 / 大模型应用开发工程师"
    )

    location: str = Field(
        default="",
        description="期望城市，如 上海 / 苏州"
    )

    salary_expectation: str = Field(
        default="",
        description="期望薪资范围，如 8-13K"
    )

    # ── 个人总结 ──
    summary: str = Field(
        default="",
        description="个人总结/概述，2-3句话突出核心竞争力"
    )

    # ── 技能标签 ──
    skills: List[str] = Field(
        default_factory=list,
        description="候选人技能列表（含编程语言、框架、工具、平台等）"
    )

    # ── 教育背景 ──
    education: List[str] = Field(
        default_factory=list,
        description="教育经历，含学校、专业、学历、时间、GPA/排名"
    )

    # ── 项目/工作经历 ──
    experience: List[str] = Field(
        default_factory=list,
        description="工作或项目经历描述"
    )

    projects: List[ProjectExperience] = Field(
        default_factory=list,
        description="结构化项目经历"
    )

    # ── 证书 & 语言 ──
    certifications: List[str] = Field(
        default_factory=list,
        description="证书与语言能力，如 CET-6、奖学金"
    )

    # ── 链接 ──
    github: str = Field(default="", description="GitHub 主页地址")
    portfolio: str = Field(default="", description="个人作品集/博客地址")

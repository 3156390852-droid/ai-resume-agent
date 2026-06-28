"""
Pydantic 模型校验测试
"""
import pytest
from app.models.resume_schema import ResumeInfo, ProjectExperience
from app.models.match_schema import MatchResult


class TestResumeInfo:
    """简历信息模型测试"""

    def test_empty_resume(self):
        """空简历也能创建（所有字段有默认值）"""
        r = ResumeInfo()
        assert r.name == ""
        assert r.skills == []
        assert r.projects == []
        assert r.desired_position == ""

    def test_full_resume(self):
        """完整简历数据"""
        r = ResumeInfo(
            name="张三",
            desired_position="AI应用工程师",
            location="上海",
            skills=["Python", "FastAPI", "LangChain"],
            projects=[
                ProjectExperience(
                    name="AI简历系统",
                    date="2026.01-2026.06",
                    stack=["FastAPI", "LangChain", "FAISS"],
                    highlights=["日均处理100份简历"],
                )
            ],
        )
        assert r.name == "张三"
        assert len(r.skills) == 3
        assert len(r.projects) == 1
        assert r.projects[0].stack == ["FastAPI", "LangChain", "FAISS"]

    def test_skills_default_empty(self):
        """skills 默认空列表"""
        r = ResumeInfo(name="测试")
        assert r.skills == []
        assert isinstance(r.skills, list)

    def test_project_defaults(self):
        """项目子模型默认值"""
        p = ProjectExperience()
        assert p.name == ""
        assert p.stack == []
        assert p.highlights == []


class TestMatchResult:
    """匹配结果模型测试"""

    def test_default_match(self):
        """最低匹配结果（match_score 为必填）"""
        m = MatchResult(match_score=0)
        assert m.match_score == 0
        assert m.matched_skills == []
        assert m.should_apply is True

    def test_full_match(self):
        """完整匹配结果"""
        m = MatchResult(
            match_score=85,
            matched_skills=["Python", "FastAPI"],
            missing_skills=["Docker", "Kubernetes"],
            reason="候选人技术栈高度匹配，缺少容器化经验但不影响核心开发。",
            suggestions=["花1-2天学习Docker基础"],
            greeting_template="您好！我是Python/FastAPI开发者...",
            interview_tips=["准备RAG架构相关问题", "复习FastAPI中间件"],
            should_apply=True,
        )
        assert m.match_score == 85
        assert len(m.matched_skills) == 2
        assert len(m.missing_skills) == 2
        assert m.should_apply is True

    def test_low_score_no_apply(self):
        """低分不建议投递"""
        m = MatchResult(match_score=30, should_apply=False)
        assert m.match_score == 30
        assert m.should_apply is False

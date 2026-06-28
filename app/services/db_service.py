"""
数据库服务 —— 使用 context manager 管理会话生命周期
"""
import json
from app.core.database import get_db
from app.models.resume_record import ResumeRecord


def save_record(filename: str, resume_text: str, resume_json: dict, jd_text: str, match_result: dict):
    """保存一条简历分析记录"""
    with get_db() as db:
        record = ResumeRecord(
            filename=filename,
            resume_text=resume_text,
            resume_json=json.dumps(resume_json, ensure_ascii=False),
            jd_text=jd_text,
            match_result=json.dumps(match_result, ensure_ascii=False),
        )
        db.add(record)


def get_records(limit: int = 10):
    """查询最近 N 条记录"""
    with get_db() as db:
        return (
            db.query(ResumeRecord)
            .order_by(ResumeRecord.id.desc())
            .limit(limit)
            .all()
        )

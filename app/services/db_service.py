import json
from app.core.database import SessionLocal
from app.models.resume_record import ResumeRecord


# =========================
# 💾 保存记录
# =========================
def save_record(filename, resume_text, resume_json, jd_text, match_result):

    db = SessionLocal()

    record = ResumeRecord(
        filename=filename,
        resume_text=resume_text,
        resume_json=json.dumps(resume_json, ensure_ascii=False),
        jd_text=jd_text,
        match_result=json.dumps(match_result, ensure_ascii=False)
    )

    db.add(record)
    db.commit()
    db.close()


# =========================
# 📖 查询历史
# =========================
def get_records(limit=10):

    db = SessionLocal()

    records = db.query(ResumeRecord).order_by(ResumeRecord.id.desc()).limit(limit).all()

    db.close()

    return records
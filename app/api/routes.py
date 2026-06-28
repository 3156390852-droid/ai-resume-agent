"""
API 路由 —— 简历上传 / 岗位匹配 / 历史记录
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from app.utils.parser import parse_resume
from app.services.llm_extractor import extract_resume_info
from app.services.job_matcher import match_resume_and_job
from app.services.db_service import save_record, get_records
from app.core.exceptions import ValidationException, FileProcessingException
from app.core.config import settings

router = APIRouter()

# ── 允许的文件类型 ──
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FIELD_LENGTH = 10_000  # 文本字段最大长度


def _validate_file(file: UploadFile):
    """校验上传文件：类型 + 大小"""
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileProcessingException(f"不支持的文件类型 '{ext}'，仅接受 PDF / Word")
    if file.size and file.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise FileProcessingException(
            f"文件过大（最大 {settings.MAX_UPLOAD_SIZE_MB}MB）"
        )


def _validate_text_field(value: str, field_name: str):
    """校验文本字段不为空且长度合理"""
    if not value or not value.strip():
        raise ValidationException(f"'{field_name}' 不能为空")
    if len(value) > MAX_FIELD_LENGTH:
        raise ValidationException(f"'{field_name}' 超过最大长度限制 {MAX_FIELD_LENGTH}")


# =========================
# 📄 上传简历 + 结构化解析
# =========================
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    _validate_file(file)

    file_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_resume(file_path)
    result = extract_resume_info(text)

    return {
        "filename": file.filename,
        "data": result.model_dump(),
    }


# =========================
# 🎯 简历 + JD 匹配
# =========================
@router.post("/match")
async def match_resume(
    resume_text: str = Form(""),
    jd_text: str = Form(""),
):
    _validate_text_field(resume_text, "resume_text")
    _validate_text_field(jd_text, "jd_text")

    result = match_resume_and_job(resume_text, jd_text)

    save_record(
        filename="manual_input",
        resume_text=resume_text,
        resume_json={},
        jd_text=jd_text,
        match_result=result.model_dump(),
    )

    return result.model_dump()


# =========================
# 📖 历史记录
# =========================
@router.get("/history")
def history():
    records = get_records()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "match_result": r.match_result,
        }
        for r in records
    ]

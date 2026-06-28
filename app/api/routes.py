"""
API 路由 —— 简历上传 / 岗位匹配 / 历史记录 / 健康检查
"""
import os
import re
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from app.utils.parser import parse_resume
from app.services.llm_extractor import extract_resume_info
from app.services.job_matcher import match_resume_and_job
from app.services.db_service import save_record, get_records
from app.core.database import engine
from app.core.exceptions import ValidationException, FileProcessingException
from app.core.logger import logger
from app.core.config import settings

router = APIRouter()

# ── 允许的文件类型 ──
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FIELD_LENGTH = 10_000  # 文本字段最大长度


def _safe_filename(filename: str) -> str:
    """安全处理文件名：去除路径穿越字符，仅保留文件名部分"""
    name = os.path.basename(filename)
    # 去除 null 字节等危险字符，仅保留可见字符
    name = re.sub(r'[\x00-\x1f]', '', name)
    if not name or name in (".", ".."):
        raise FileProcessingException("无效的文件名")
    return name


def _validate_file(file: UploadFile):
    """校验上传文件：类型 + 大小"""
    filename = _safe_filename(file.filename or "")
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileProcessingException(f"不支持的文件类型 '{ext}'，仅接受 PDF / Word")
    if file.size and file.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise FileProcessingException(
            f"文件过大（最大 {settings.MAX_UPLOAD_SIZE_MB}MB）"
        )
    return filename


def _validate_text_field(value: str, field_name: str):
    """校验文本字段不为空且长度合理"""
    if not value or not value.strip():
        raise ValidationException(f"'{field_name}' 不能为空")
    if len(value) > MAX_FIELD_LENGTH:
        raise ValidationException(f"'{field_name}' 超过最大长度限制 {MAX_FIELD_LENGTH}")


# =========================
# 📄 上传简历 + 结构化解析
# =========================
@router.post(
    "/upload-resume",
    tags=["简历解析"],
    summary="上传简历并提取结构化信息",
    description="支持 PDF / Word 格式，使用 LLM 提取姓名、技能、教育、项目经历等结构化信息。",
)
async def upload_resume(file: UploadFile = File(...)):
    safe_name = _validate_file(file)

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{safe_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_resume(file_path)
    result = extract_resume_info(text)

    # 持久化简历数据（不含匹配结果），DB 故障不影响返回
    try:
        save_record(
            filename=safe_name,
            resume_text=text,
            resume_json=result.model_dump(),
            jd_text="",
            match_result={},
        )
    except Exception:
        logger.warning("简历数据保存失败，但不影响解析结果返回")

    return {
        "filename": safe_name,
        "data": result.model_dump(),
    }


# =========================
# 🎯 简历 + JD 匹配
# =========================
@router.post(
    "/match",
    tags=["岗位匹配"],
    summary="简历与岗位 JD 匹配分析",
    description="输入简历文本和岗位 JD，结合行业知识库进行语义匹配，输出评分、技能缺口、学习建议、招呼语和投递决策。",
)
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
@router.get(
    "/history",
    tags=["系统"],
    summary="查询历史匹配记录",
    description="返回最近 10 条分析记录，含文件名和匹配结果。",
)
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


# =========================
# 🏥 健康检查
# =========================
@router.get(
    "/health",
    tags=["系统"],
    summary="健康检查",
    description="检查服务运行状态和数据库连通性。",
)
def health():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    return {
        "status": "ok",
        "database": db_status,
    }

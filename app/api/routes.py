from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from app.utils.parser import parse_resume
from app.services.llm_extractor import extract_resume_info
from app.services.job_matcher import match_resume_and_job
from app.services.db_service import save_record, get_records

router = APIRouter()

# =========================
# 📄 上传简历 + 结构化解析
# =========================
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    #保存文件路径
    file_path = f"data/{file.filename}"

    # 保存文件,写入硬盘
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 解析文本，变成纯文本
    text = parse_resume(file_path)

    # LLM结构化，整理为JSON
    result = extract_resume_info(text)

    return {
        "filename": file.filename,
        "data": result.model_dump()
    }


# =========================
# 🎯 简历 + JD 匹配
# =========================
@router.post("/match")
async def match_resume(
    resume_text: str = Form(...),
    jd_text: str = Form(...)
):

    result = match_resume_and_job(resume_text, jd_text)

    # 💾 保存到数据库（关键）
    save_record(
        filename="manual_input",
        resume_text=resume_text,
        resume_json={},
        jd_text=jd_text,
        match_result=result.model_dump()
    )

    return result.model_dump()

@router.get("/history")
def history():

    records = get_records()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "match_result": r.match_result
        }
        for r in records
    ]
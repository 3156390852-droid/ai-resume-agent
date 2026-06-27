from pypdf import PdfReader
import docx


# =========================
# 1️⃣ 解析 PDF
# =========================
def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# =========================
# 2️⃣ 解析 Word
# =========================
def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# =========================
# 3️⃣ 自动识别格式
# =========================
def parse_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError("不支持的文件格式")
    

from app.core.logger import logger

def parse_resume(file_path: str) -> str:
    try:
        logger.info(f"开始解析简历: {file_path}")

        # 原解析逻辑
        text = "..."

        logger.info("简历解析成功")
        return text

    except Exception as e:
        logger.error(f"简历解析失败: {str(e)}")
        raise e
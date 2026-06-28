"""
简历文件解析 —— 支持 PDF / Word，自动识别格式
"""
from functools import wraps
from pypdf import PdfReader
import docx
from app.core.logger import logger
from app.core.exceptions import FileProcessingException


def _log_parse(func):
    """装饰器：为解析函数添加日志"""
    @wraps(func)
    def wrapper(file_path: str) -> str:
        try:
            logger.info("开始解析简历: %s", file_path)
            text = func(file_path)
            logger.info("简历解析成功，提取 %d 字符", len(text))
            return text
        except FileProcessingException:
            raise
        except Exception as e:
            logger.error("简历解析失败: %s", str(e))
            raise FileProcessingException(f"文件解析失败: {str(e)}") from e
    return wrapper


def parse_pdf(file_path: str) -> str:
    """解析 PDF 文件"""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


def parse_docx(file_path: str) -> str:
    """解析 Word 文件"""
    doc = docx.Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)


@_log_parse
def parse_resume(file_path: str) -> str:
    """自动识别文件格式并解析简历"""
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise FileProcessingException(f"不支持的文件格式: {file_path}，仅支持 .pdf / .docx")

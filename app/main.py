"""
FastAPI 应用入口
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.exceptions import AppException
from app.core.logger import logger

DESCRIPTION = """
AI Resume Agent —— 智能简历解析与岗位匹配系统

- 📄 上传 PDF/Word 简历，自动提取结构化信息
- 🎯 简历与 JD 语义匹配，输出评分 + 技能缺口 + 学习建议
- 💬 生成 BOSS 直聘招呼语模板和面试准备建议
- ✅ 给出投递决策（是否建议投递）
- 📖 历史记录查询
"""

app = FastAPI(
    title="AI Resume Agent",
    description=DESCRIPTION,
    version="1.0.0",
)

# ── CORS 中间件 ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["系统"])
def root():
    """服务运行状态检查"""
    return {"message": "AI Resume Agent Running"}


# ── 业务异常处理器（按状态码区分） ──
@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException):
    logger.warning("业务异常 [%s]: %s", exc.__class__.__name__, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "detail": str(exc) if str(exc) != exc.message else ""},
    )


# ── 未捕获异常兜底 ──
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("未捕获异常: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": "系统内部错误，请稍后重试"},
    )

"""
FastAPI 应用入口
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.exceptions import AppException
from app.core.logger import logger


app = FastAPI(title="AI Resume Agent")

app.include_router(router)


@app.get("/")
def root():
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

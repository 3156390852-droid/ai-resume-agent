# from app.utils.parser import parse_resume
# from app.services.job_matcher import match_resume_and_job

# resume_text = parse_resume("data/test_resume.pdf")

# jd_text = """
# Python后端开发实习生

# 要求：
# - 熟悉Python
# - 熟悉FastAPI或Flask
# - 熟悉MySQL
# - 了解Docker优先
# - 有项目经验优先
# """

# result = match_resume_and_job(resume_text, jd_text)

# print(result.model_dump())
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router

app = FastAPI(title="AI Resume Agent")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI Resume Agent Running"}



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "系统异常",
            "error": str(exc)
        }
    )
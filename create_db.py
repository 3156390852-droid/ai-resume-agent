from app.core.database import Base, engine
from app.models.resume_record import ResumeRecord

Base.metadata.create_all(bind=engine)

print("数据库初始化完成")
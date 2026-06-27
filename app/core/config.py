import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    MODEL_NAME = os.getenv("MODEL_NAME")

    MYSQL_URL = os.getenv("MYSQL_URL")


settings = Settings()
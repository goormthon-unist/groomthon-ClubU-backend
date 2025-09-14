import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLite 데이터베이스 설정 (테스트용)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///clubu_test.db")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

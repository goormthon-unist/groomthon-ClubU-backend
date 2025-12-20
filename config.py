import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLite 데이터베이스 설정 (테스트용)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///clubu_test.db")

    # MySQL 연결 옵션 (타임존 설정 포함)
    # SQLite인 경우 connect_args를 추가하지 않음
    engine_options = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }

    # MySQL인 경우에만 타임존 설정 추가 (RDS 파라미터 그룹과 일치)
    if (
        "mysql" in os.getenv("DATABASE_URL", "").lower()
        or "mariadb" in os.getenv("DATABASE_URL", "").lower()
    ):
        engine_options["connect_args"] = {"init_command": "SET time_zone='Asia/Seoul'"}

    SQLALCHEMY_ENGINE_OPTIONS = engine_options

    # 파일 저장 경로 설정
    BANNERS_DIR = os.getenv("BANNERS_DIR", "banners")
    CLUBS_DIR = os.getenv("CLUBS_DIR", "clubs")
    NOTICES_DIR = os.getenv("NOTICES_DIR", "notices")
    RESERVATIONS_DIR = os.getenv("RESERVATIONS_DIR", "reservations")

    # 파일 업로드 크기 제한 설정 (500MB)
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

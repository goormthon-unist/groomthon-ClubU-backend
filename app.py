import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api

# 환경변수 로드
load_dotenv()

# 데이터베이스 객체 import
from models import db


def create_app():
    app = Flask(__name__)

    # 설정 로드
    from config import config

    app.config.from_object(config[os.getenv("FLASK_ENV", "development")])

    # CORS 설정
    CORS(app)

    # 데이터베이스 초기화
    db.init_app(app)

    # 마이그레이션 초기화
    Migrate(app, db)

    # Flask-RESTX API 초기화
    api = Api(
        app,
        version="1.0",
        title="ClubU API",
        description="UNIST 동아리 관리 시스템 API",
        doc="/docs/",  # Swagger UI 경로
    )

    # 네임스페이스 등록
    from routes.club_routes import club_ns
    from routes import init_app as init_routes

    api.add_namespace(club_ns, path="/api/v1/clubs")
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

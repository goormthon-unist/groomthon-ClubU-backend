import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

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

    # 블루프린트 등록
    from routes import init_app as init_routes

    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

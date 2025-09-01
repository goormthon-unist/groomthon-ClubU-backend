import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api

from models import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    # 설정 로드
    from config import config

    app.config.from_object(config[os.getenv("FLASK_ENV", "development")])

    # Flask 세션 설정 추가
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

    # HTTPS 강제 설정 (api.clubu.co.kr 도메인 사용)
    app.config["SESSION_COOKIE_SECURE"] = True  # HTTPS에서만 쿠키 설정
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "None"  # HTTPS에서 크로스 사이트 요청 허용
    app.config["SESSION_COOKIE_DOMAIN"] = None
    app.config["SESSION_COOKIE_PATH"] = "/"

    # CORS 설정 (HTTPS 환경에 맞춤)
    allowed_origins = [
        "https://clubu.co.kr",
        "https://www.clubu.co.kr",
        "https://api.clubu.co.kr",
    ]

    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # DB & Migrate 초기화
    db.init_app(app)
    Migrate(app, db)

    # RESTX API
    api = Api(
        app,
        version="1.0",
        title="ClubU API",
        description="UNIST 동아리 관리 시스템 API",
        doc="/docs/",
    )

    # 네임스페이스 등록
    from routes.home_routes import home_ns
    from routes.question_routes import question_ns
    from routes.application_check_submit_routes import application_ns

    from routes.auth_routes import auth_ns
    from routes.role_routes import role_ns
    from routes.application_check_routes import application_check_ns
    from routes import init_app as init_routes

    api.add_namespace(home_ns, path="/api/v1/clubs")
    api.add_namespace(question_ns, path="/api/v1")
    api.add_namespace(application_ns, path="/api/v1")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(role_ns, path="/api/v1/roles")
    api.add_namespace(application_check_ns, path="/api/v1")
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

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

    # 쿠키 설정 (개발/프로덕션 환경 고려)
    is_production = os.getenv("FLASK_ENV") == "production"

    app.config["SESSION_COOKIE_SECURE"] = is_production  # 프로덕션에서만 HTTPS 강제
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = (
        "None" if is_production else "Lax"
    )  # 개발환경에서는 Lax
    app.config["SESSION_COOKIE_DOMAIN"] = None
    app.config["SESSION_COOKIE_PATH"] = "/"

    # CORS 설정 (개발/프로덕션 환경 모두 지원)
    allowed_origins = [
        # 프로덕션 도메인 (클라이언트가 실행되는 도메인)
        "https://clubu.co.kr",
        "https://www.clubu.co.kr",
        "https://api.clubu.co.kr",
        # 개발 환경 (localhost)
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]

    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
        ],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["Set-Cookie"],
    )

    # DB & Migrate 초기화
    db.init_app(app)
    Migrate(app, db)

    # 정적 파일 서빙 설정
    from flask import send_from_directory

    @app.route("/banners/<path:filename>")
    def serve_banner(filename):
        return send_from_directory("banners", filename)

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
    from routes.notice_routes import notice_ns, club_notice_ns
    from routes.banner_routes import banner_ns

    from routes.auth_routes import auth_ns
    from routes.role_routes import role_ns
    from routes.application_check_routes import application_check_ns
    from routes.user_routes import user_ns
    from routes.admin_routes import admin_ns
    from routes.department_routes import department_ns
    from routes import init_app as init_routes

    api.add_namespace(home_ns, path="/api/v1/clubs")
    api.add_namespace(question_ns, path="/api/v1")
    api.add_namespace(application_ns, path="/api/v1")
    api.add_namespace(notice_ns, path="/api/v1")
    api.add_namespace(club_notice_ns, path="/api/v1/clubs")
    api.add_namespace(banner_ns, path="/api/v1")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(role_ns, path="/api/v1/roles")
    api.add_namespace(application_check_ns, path="/api/v1")
    api.add_namespace(user_ns, path="/api/v1/users")
    api.add_namespace(admin_ns, path="/api/v1/admin")
    api.add_namespace(department_ns, path="/api/v1/departments")
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

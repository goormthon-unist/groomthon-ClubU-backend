import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api

# 데이터베이스 객체 import
from models import db

# 환경변수 로드
load_dotenv()


def create_app():
    app = Flask(__name__)

    # 설정 로드
    from config import config

    app.config.from_object(config[os.getenv("FLASK_ENV", "development")])
    
    # Flask 세션 설정 추가
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SESSION_COOKIE_SECURE'] = False  # 개발환경에서는 False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_DOMAIN'] = None  # 모든 도메인에서 접근 가능
    app.config['SESSION_COOKIE_PATH'] = '/'

    # CORS 설정 (쿠키 지원)
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

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
    from routes.home_routes import home_ns
    from routes.application_check_submit_routes import application_ns
    from routes.auth_routes import auth_ns
    from routes.role_routes import role_ns
    from routes import init_app as init_routes

    api.add_namespace(home_ns, path="/api/v1/clubs")
    api.add_namespace(application_ns, path="/api/v1")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(role_ns, path="/api/v1/roles")
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

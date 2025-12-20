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

    # 파일 업로드 크기 제한 강제 설정
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB

    # 인코딩 설정
    app.config["JSON_AS_ASCII"] = False  # JSON에서 한글 지원
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    # Werkzeug 설정 (더 낮은 레벨에서 제한)
    from werkzeug.serving import WSGIRequestHandler

    WSGIRequestHandler.max_request_line_size = 500 * 1024 * 1024  # 500MB

    # Flask 세션 설정 추가
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

    # 쿠키 설정 (개발/프로덕션 환경 고려)
    is_production = os.getenv("FLASK_ENV") == "production"

    app.config["SESSION_COOKIE_SECURE"] = is_production  # 프로덕션에서만 HTTPS 강제
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = (
        "None"  # 크로스 사이트 요청에서도 쿠키 전송 허용
    )
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
        resources={r"/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
        ],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["Set-Cookie", "Content-Type"],
        max_age=3600,
    )

    # OPTIONS 요청 명시적 처리 (preflight 요청)
    @app.before_request
    def handle_preflight():
        from flask import request, make_response

        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            # 허용된 Origin인지 확인
            if origin in allowed_origins:
                response = make_response()
                response.headers.add("Access-Control-Allow-Origin", origin)
                response.headers.add(
                    "Access-Control-Allow-Headers",
                    "Content-Type, Authorization, X-Requested-With, Accept, Origin",
                )
                response.headers.add(
                    "Access-Control-Allow-Methods",
                    "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                )
                response.headers.add("Access-Control-Allow-Credentials", "true")
                response.headers.add("Access-Control-Max-Age", "3600")
                return response

    # DB & Migrate 초기화
    db.init_app(app)
    Migrate(app, db)

    # 정적 파일 서빙 설정
    from flask import send_from_directory

    @app.route("/banners/<path:filename>")
    def serve_banner(filename):
        banners_dir = app.config.get("BANNERS_DIR", "banners")
        # 절대 경로로 변환
        if not os.path.isabs(banners_dir):
            banners_dir = os.path.join(app.root_path, banners_dir)
        return send_from_directory(banners_dir, filename)

    @app.route("/clubs/<path:filename>")
    def serve_club_image(filename):
        clubs_dir = app.config.get("CLUBS_DIR", "clubs")
        # 절대 경로로 변환
        if not os.path.isabs(clubs_dir):
            clubs_dir = os.path.join(app.root_path, clubs_dir)
        return send_from_directory(clubs_dir, filename)

    @app.route("/reservations/<path:filename>")
    def serve_reservation_file(filename):
        reservations_dir = app.config.get("RESERVATIONS_DIR", "reservations")
        # 절대 경로로 변환
        if not os.path.isabs(reservations_dir):
            reservations_dir = os.path.join(app.root_path, reservations_dir)
        return send_from_directory(reservations_dir, filename)

    @app.route("/notices/<path:filename>")
    def serve_notice_file(filename):
        from flask import current_app, abort

        notices_dir = app.config.get("NOTICES_DIR", "notices")
        # 절대 경로로 변환
        if not os.path.isabs(notices_dir):
            notices_dir = os.path.join(app.root_path, notices_dir)

        # 파일 경로 구성
        file_path = os.path.join(notices_dir, filename)

        # 파일 존재 확인
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            current_app.logger.error(
                f"File not found: {file_path} (notices_dir: {notices_dir}, filename: {filename})"
            )
            abort(404)

        # 파일 서빙
        return send_from_directory(notices_dir, filename)

    # 413 오류 핸들러 추가
    @app.errorhandler(413)
    def too_large(e):
        from flask import jsonify, current_app

        current_app.logger.error(f"413 Error: {e}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "파일 크기가 너무 큽니다. 최대 500MB까지 업로드 가능합니다.",
                    "code": "413-01",
                }
            ),
            413,
        )

    # RESTX API
    api = Api(
        app,
        version="1.0",
        title="ClubU API",
        description="UNIST 동아리 관리 시스템 API<br><div id='server-time' style='margin-top: 10px; padding: 8px; background: #f0f0f0; border-radius: 4px; font-family: monospace;'><strong>서버 시간 (KST):</strong> <span id='time-display'>로딩 중...</span></div>",
        doc="/docs/",
        authorizations={
            "sessionAuth": {"type": "apiKey", "in": "cookie", "name": "session"}
        },
        # Swagger UI에서 쿠키 전송 및 서버 시간 표시를 위한 설정
        swagger_ui_params={
            "requestInterceptor": """
                function(request) {
                    // 모든 요청에 credentials 포함
                    request.credentials = 'include';
                    return request;
                }
            """,
            "onComplete": """
                function() {
                    // 서버 시간 업데이트 함수
                    function updateServerTime() {
                        fetch('/health')
                            .then(response => response.json())
                            .then(data => {
                                if (data.server_time) {
                                    const timeDisplay = document.getElementById('time-display');
                                    if (timeDisplay) {
                                        timeDisplay.textContent = data.server_time.formatted;
                                    }
                                }
                            })
                            .catch(error => {
                                console.error('서버 시간 가져오기 실패:', error);
                            });
                    }
                    
                    // 초기 로드 시 서버 시간 가져오기
                    updateServerTime();
                    
                    // 1초마다 서버 시간 업데이트
                    setInterval(updateServerTime, 1000);
                }
            """,
        },
    )

    # 네임스페이스 등록
    from routes.home_routes import home_ns
    from routes.application_check_submit_routes import application_ns
    from routes.notice_routes import notice_ns, club_notice_ns
    from routes.notice_asset_routes import notice_asset_ns
    from routes.file_download_routes import file_download_ns
    from routes.banner_routes import banner_ns

    from routes.auth_routes import auth_ns
    from routes.role_routes import role_ns
    from routes.application_check_routes import application_check_ns
    from routes.user_routes import user_ns
    from routes.admin_user_role_routes import admin_user_role_ns
    from routes.club_member_role_routes import club_member_role_ns
    from routes.department_routes import department_ns
    from routes.club_info_routes import club_info_ns
    from routes.user_search_routes import user_search_ns
    from routes.room_routes import room_ns
    from routes.reservation_routes import reservation_ns
    from routes.club_room_routes import club_room_ns
    from routes.cleaning_routes import cleaning_ns
    from routes import init_app as init_routes

    api.add_namespace(home_ns, path="/api/v1/clubs")
    api.add_namespace(application_ns, path="/api/v1")
    api.add_namespace(notice_ns, path="/api/v1")
    api.add_namespace(club_notice_ns, path="/api/v1/clubs")
    api.add_namespace(notice_asset_ns, path="/api/v1")
    api.add_namespace(file_download_ns, path="/api/v1")
    api.add_namespace(banner_ns, path="/api/v1/banners")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(role_ns, path="/api/v1/roles")
    api.add_namespace(application_check_ns, path="/api/v1")
    api.add_namespace(user_ns, path="/api/v1/users")
    api.add_namespace(admin_user_role_ns, path="/api/v1/admin")
    api.add_namespace(club_member_role_ns, path="/api/v1/clubs")
    api.add_namespace(department_ns, path="/api/v1/departments")
    api.add_namespace(club_info_ns, path="/api/v1/clubs")
    api.add_namespace(user_search_ns, path="/api/v1/users")
    api.add_namespace(room_ns, path="/api/v1/rooms")
    api.add_namespace(reservation_ns, path="/api/v1/reservations")
    api.add_namespace(club_room_ns, path="/api/v1/clubs")
    api.add_namespace(cleaning_ns, path="/api/v1")
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

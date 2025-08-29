from flask import Blueprint

# 메인 블루프린트
main_bp = Blueprint("main", __name__)

# 모든 라우트를 여기서 import
from .club import club_bp


# 헬스체크 엔드포인트
@main_bp.route("/health")
def health_check():
    """서버 상태 확인용 헬스체크 엔드포인트"""
    from flask import jsonify
    from models import db

    try:
        # 데이터베이스 연결 상태 확인
        db.session.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify(
        {
            "status": "healthy",
            "message": "ClubU Backend API is running",
            "database": db_status,
        }
    )


@main_bp.route("/")
def root():
    """루트 엔드포인트"""
    from flask import jsonify

    return jsonify(
        {
            "message": "Welcome to ClubU API",
            "version": "1.0.0",
            "endpoints": {"health": "/health", "clubs": "/api/v1/clubs"},
        }
    )


# 블루프린트 등록
def init_app(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(club_bp, url_prefix="/api/v1/clubs")

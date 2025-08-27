from flask import Blueprint

# 메인 블루프린트
main_bp = Blueprint('main', __name__)

# 모든 라우트를 여기서 import
from .club import club_bp

# 블루프린트 등록
def init_app(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(club_bp, url_prefix='/api/v1/clubs')

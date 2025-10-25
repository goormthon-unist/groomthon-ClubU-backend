from flask_restx import Namespace
from controllers.cleaning_controller import cleaning_ns

# 청소 사진 관리 라우트
# 이 네임스페이스는 app.py에서 /api/v1 경로에 등록됩니다.
# 따라서 이 네임스페이스 내의 라우트는 /api/v1/cleaning/... 형태가 됩니다.

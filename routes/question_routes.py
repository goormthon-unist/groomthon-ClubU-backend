from flask_restx import Namespace
from controllers.home_controller import QuestionController

# 네임스페이스 등록
question_ns = Namespace("application/questions", description="지원서 문항 관리 API")


# API 엔드포인트 등록
@question_ns.route("/<int:question_id>")
class QuestionResource(QuestionController):
    """지원서 문항 수정/삭제 리소스"""

    pass

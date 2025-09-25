from flask_restx import Namespace, fields
from controllers.home_controller import QuestionController

# 네임스페이스 등록
question_ns = Namespace("application/questions", description="지원서 문항 관리 API")

# Swagger 모델 정의
question_update_model = question_ns.model(
    "QuestionUpdate",
    {
        "question_text": fields.String(required=True, description="수정할 질문 내용"),
    },
)


# API 엔드포인트 등록
@question_ns.route("/<int:question_id>")
class QuestionResource(QuestionController):
    """지원서 문항 수정/삭제 리소스"""

    @question_ns.expect(question_update_model)
    def patch(self, question_id):
        """지원서 문항 수정"""
        return super().patch(question_id)

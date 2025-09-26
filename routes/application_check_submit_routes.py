from flask_restx import Namespace, fields
from controllers.application_check_submit_controller import (
    ApplicationSubmitController,
)

# 네임스페이스 등록
application_ns = Namespace("applications", description="지원서 관리 API")

# Swagger 모델 정의
application_submit_model = application_ns.model(
    "ApplicationSubmit",
    {
        "answers": fields.List(
            fields.Nested(
                application_ns.model(
                    "Answer",
                    {
                        "question_id": fields.Integer(
                            required=True, description="질문 ID"
                        ),
                        "answer_text": fields.String(
                            required=True, description="답변 내용"
                        ),
                    },
                )
            ),
            required=True,
            description="지원서 답변 목록",
        )
    },
)


# API 엔드포인트 등록


@application_ns.route("/applications/<int:club_id>")
class ApplicationSubmitResource(ApplicationSubmitController):
    """지원서 제출 리소스"""

    @application_ns.expect(application_submit_model)
    def post(self, club_id):
        """지원서 제출"""
        return super().post(club_id)

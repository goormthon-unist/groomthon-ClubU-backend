from flask_restx import Namespace
from controllers.application_check_submit_controller import (
    ClubApplicationQuestionsController,
    ApplicationSubmitController,
)

# 네임스페이스 등록
application_ns = Namespace("applications", description="지원서 관리 API")


# 임시 테스트 API
@application_ns.route("/test")
class TestResource:
    """테스트용 임시 API"""

    def get(self):
        return {"message": "테스트 API 성공!", "status": "ok"}, 200


# API 엔드포인트 등록
@application_ns.route("/clubs/<int:club_id>/application/questions")
class ClubApplicationQuestionsResource(ClubApplicationQuestionsController):
    """동아리 지원 질문 조회 리소스"""

    pass


@application_ns.route("/applications/<int:club_id>")
class ApplicationSubmitResource(ApplicationSubmitController):
    """지원서 제출 리소스"""

    pass

from flask_restx import Namespace
from controllers.home_controller import (
    ClubListController,
    ClubUpdateController,
    ClubStatusController,
    ClubQuestionsController,
    ClubMembersController,
    QuestionController,
)

# 네임스페이스 등록
home_ns = Namespace("clubs", description="동아리 관리 API")


# API 엔드포인트 등록
@home_ns.route("/")
class ClubListResource(ClubListController):
    """동아리 목록 조회 리소스"""

    pass


@home_ns.route("/<int:club_id>")
class ClubDetailResource(ClubUpdateController):
    """동아리 상세 조회 및 정보 수정 리소스"""

    pass


@home_ns.route("/<int:club_id>/status")
class ClubStatusResource(ClubStatusController):
    """동아리 모집 상태 변경 리소스"""

    pass


@home_ns.route("/<int:club_id>/application/questions")
class ClubQuestionsResource(ClubQuestionsController):
    """동아리 지원서 문항 추가 리소스"""

    pass


@home_ns.route("/<int:club_id>/members")
class ClubMembersResource(ClubMembersController):
    """동아리원 목록 조회 리소스"""

    pass


# 문항 수정/삭제 엔드포인트
@home_ns.route("/application/questions/<int:question_id>")
class QuestionResource(QuestionController):
    """지원서 문항 수정/삭제 리소스"""

    pass

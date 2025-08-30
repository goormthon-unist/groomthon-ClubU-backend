from flask_restx import Namespace
from controllers.home_controller import (
    ClubListController, ClubDetailController, ClubUpdateController,
    ClubStatusController, ClubQuestionsController, ClubMembersController,
    OpenClubsController
)

# 네임스페이스 등록
home_ns = Namespace("clubs", description="동아리 관리 API")


# API 엔드포인트 등록
@home_ns.route("/")
class ClubListResource(ClubListController):
    """동아리 목록 조회 리소스"""

    pass


@home_ns.route("/<int:club_id>")
class ClubDetailResource(ClubDetailController):
    """동아리 상세 조회 리소스"""

    pass


@home_ns.route("/<int:club_id>/update")
class ClubUpdateResource(ClubUpdateController):
    """동아리 정보 수정 리소스"""

    pass


@home_ns.route("/<int:club_id>/status")
class ClubStatusResource(ClubStatusController):
    """동아리 모집 상태 변경 리소스"""

    pass


@home_ns.route("/<int:club_id>/application/questions")
class ClubQuestionsResource(ClubQuestionsController):
    """동아리 지원서 문항 관리 리소스"""

    pass


@home_ns.route("/<int:club_id>/members")
class ClubMembersResource(ClubMembersController):
    """동아리원 목록 조회 리소스"""

    pass


@home_ns.route("/imminent")
class OpenClubsResource(OpenClubsController):
    """모집 중인 동아리 조회 리소스"""

    pass

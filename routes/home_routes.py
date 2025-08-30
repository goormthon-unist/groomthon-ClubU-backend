from flask_restx import Namespace
from controllers.home_controller import ClubListController, ClubDetailController, OpenClubsController

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


@home_ns.route("/imminent")
class OpenClubsResource(OpenClubsController):
    """모집 중인 동아리 조회 리소스"""

    pass

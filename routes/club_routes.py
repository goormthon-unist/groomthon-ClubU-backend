from flask_restx import Namespace
from controllers.club_controller import ClubListController, ClubDetailController

# 네임스페이스 등록
club_ns = Namespace("clubs", description="동아리 관리 API")


# API 엔드포인트 등록
@club_ns.route("/")
class ClubListResource(ClubListController):
    """동아리 목록 조회 리소스"""

    pass


@club_ns.route("/<int:club_id>")
class ClubDetailResource(ClubDetailController):
    """동아리 상세 조회 리소스"""

    pass

from flask_restx import Namespace
from controllers.club_info_controller import (
    ClubIntroductionController,
    ClubLogoImageController,
    ClubIntroductionImageController,
)

# 네임스페이스 등록
club_info_ns = Namespace("club-info", description="동아리 정보 수정 API")


# 동아리 소개글 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/introduction")
class ClubIntroductionResource(ClubIntroductionController):
    """동아리 소개글 관리 리소스"""

    pass


# 동아리 로고 이미지 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/images/logo")
class ClubLogoImageResource(ClubLogoImageController):
    """동아리 로고 이미지 관리 리소스"""

    pass


# 동아리 소개글 이미지 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/images/introduction")
class ClubIntroductionImageResource(ClubIntroductionImageController):
    """동아리 소개글 이미지 관리 리소스"""

    pass

from flask_restx import Namespace, reqparse
from werkzeug.datastructures import FileStorage
from controllers.club_info_controller import (
    ClubIntroductionController,
    ClubLogoImageController,
    ClubIntroductionImageController,
)

# 네임스페이스 등록
club_info_ns = Namespace("club-info", description="동아리 정보 수정 API")

# RequestParser 정의 (동아리 이미지 업로드용)
logo_image_parser = reqparse.RequestParser()
logo_image_parser.add_argument(
    "image",
    type=FileStorage,
    location="files",
    required=True,
    help="동아리 로고 이미지 파일",
)

introduction_image_parser = reqparse.RequestParser()
introduction_image_parser.add_argument(
    "image",
    type=FileStorage,
    location="files",
    required=True,
    help="동아리 소개글 이미지 파일",
)


# 동아리 소개글 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/introduction")
class ClubIntroductionResource(ClubIntroductionController):
    """동아리 소개글 관리 리소스"""

    pass


# 동아리 로고 이미지 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/images/logo")
class ClubLogoImageResource(ClubLogoImageController):
    """동아리 로고 이미지 관리 리소스"""

    @club_info_ns.expect(logo_image_parser)
    @club_info_ns.doc("upload_club_logo", consumes=["multipart/form-data"])
    def put(self, club_id):
        """동아리 로고 이미지 업로드/수정"""
        return super().put(club_id)

    @club_info_ns.doc("delete_club_logo")
    def delete(self, club_id):
        """동아리 로고 이미지 삭제"""
        return super().delete(club_id)


# 동아리 소개글 이미지 관리 엔드포인트
@club_info_ns.route("/<int:club_id>/images/introduction")
class ClubIntroductionImageResource(ClubIntroductionImageController):
    """동아리 소개글 이미지 관리 리소스"""

    @club_info_ns.expect(introduction_image_parser)
    @club_info_ns.doc(
        "upload_club_introduction_image", consumes=["multipart/form-data"]
    )
    def put(self, club_id):
        """동아리 소개글 이미지 업로드/수정"""
        return super().put(club_id)

    @club_info_ns.doc("delete_club_introduction_image")
    def delete(self, club_id):
        """동아리 소개글 이미지 삭제"""
        return super().delete(club_id)

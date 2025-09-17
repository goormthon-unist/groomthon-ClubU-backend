from flask_restx import Namespace, fields
from controllers.notice_controller import (
    ClubNoticeController,
    NoticeController,
    NoticeDetailController,
    ClubNoticeDetailController,
)

# 네임스페이스 등록
notice_ns = Namespace("notices", description="공지 관리 API")
club_notice_ns = Namespace("club-notices", description="동아리 공지 관리 API")

# Request Body 모델 정의
club_notice_model = club_notice_ns.model(
    "ClubNotice",
    {
        "title": fields.String(required=True, description="공지 제목"),
        "content": fields.String(required=True, description="공지 내용"),
        "is_important": fields.Boolean(
            required=False, description="중요 공지 여부", default=False
        ),
    },
)


# 동아리 공지 관리 엔드포인트
@club_notice_ns.route("/<int:club_id>/notices")
class ClubNoticeResource(ClubNoticeController):
    """동아리 공지 관리 리소스"""

    @club_notice_ns.doc("create_club_notice")
    @club_notice_ns.expect(club_notice_model)
    @club_notice_ns.response(201, "공지 등록 성공")
    @club_notice_ns.response(400, "잘못된 요청")
    @club_notice_ns.response(401, "로그인이 필요합니다")
    @club_notice_ns.response(500, "서버 내부 오류")
    def post(self, club_id):
        """동아리 공지 등록"""
        return super().post(club_id)


@club_notice_ns.route("/<int:club_id>/notices/<int:notice_id>")
class ClubNoticeDetailResource(ClubNoticeDetailController):
    """동아리 공지 상세 관리 리소스"""

    pass


# 전체 공지 관리 엔드포인트
@notice_ns.route("/notices/")
class NoticeResource(NoticeController):
    """전체 공지 관리 리소스"""

    pass


@notice_ns.route("/notices/<int:notice_id>")
class NoticeDetailResource(NoticeDetailController):
    """공지 상세 관리 리소스"""

    pass

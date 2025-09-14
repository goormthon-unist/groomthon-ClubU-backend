from flask_restx import Namespace
from controllers.notice_controller import (
    ClubNoticeController,
    NoticeController,
    NoticeDetailController,
    ClubNoticeDetailController,
)

# 네임스페이스 등록
notice_ns = Namespace("notices", description="공지 관리 API")
club_notice_ns = Namespace("club-notices", description="동아리 공지 관리 API")


# 동아리 공지 관리 엔드포인트
@club_notice_ns.route("/<int:club_id>/notices")
class ClubNoticeResource(ClubNoticeController):
    """동아리 공지 관리 리소스"""
    pass


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

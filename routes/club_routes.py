from flask_restx import Namespace
from controllers.club_controller import (
    ClubListController, 
    ClubDetailController, 
    ClubStatusController,
    ClubMembersController,
    ClubQuestionsController,
    QuestionDetailController
)

# 네임스페이스 등록
club_ns = Namespace("clubs", description="동아리 관리 API")


# API 엔드포인트 등록
@club_ns.route("/")
class ClubListResource(ClubListController):
    """동아리 목록 조회 리소스"""
    pass


@club_ns.route("/<int:club_id>")
class ClubDetailResource(ClubDetailController):
    """동아리 상세 조회/수정 리소스"""
    pass


@club_ns.route("/<int:club_id>/status")
class ClubStatusResource(ClubStatusController):
    """동아리 모집 상태 변경 리소스"""
    pass


@club_ns.route("/<int:club_id>/members")
class ClubMembersResource(ClubMembersController):
    """동아리원 목록 조회 리소스"""
    pass


@club_ns.route("/<int:club_id>/application/questions")
class ClubQuestionsResource(ClubQuestionsController):
    """동아리 지원서 문항 조회/추가 리소스"""
    pass


# 별도 네임스페이스로 문항 관리
application_ns = Namespace("application", description="지원서 문항 관리 API")


@application_ns.route("/questions/<int:question_id>")
class QuestionDetailResource(QuestionDetailController):
    """지원서 문항 수정/삭제 리소스"""
    pass

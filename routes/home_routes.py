from flask_restx import Namespace, fields
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

# Swagger 모델 정의
club_question_create_model = home_ns.model(
    "ClubQuestionCreate",
    {
        "question_text": fields.String(required=True, description="지원서 질문 내용"),
    },
)

club_question_update_model = home_ns.model(
    "ClubQuestionUpdate",
    {
        "question_text": fields.String(required=True, description="수정할 질문 내용"),
    },
)


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

    @home_ns.expect(club_question_create_model)
    def post(self, club_id):
        """동아리 지원서 문항 추가"""
        return super().post(club_id)


@home_ns.route("/<int:club_id>/members")
class ClubMembersResource(ClubMembersController):
    """동아리원 목록 조회 리소스"""

    pass


# 모집 중인 동아리 조회 엔드포인트
@home_ns.route("/imminent")
class OpenClubsResource(ClubListController):
    """모집 중인 동아리 조회 리소스"""

    def get(self):
        """모집 중인 동아리 목록을 반환합니다"""
        from services.home_service import get_open_clubs
        from flask_restx import abort

        try:
            clubs_data = get_open_clubs()

            # 모집 중인 동아리가 없는 경우
            if not clubs_data:
                return {
                    "ok": True,
                    "data": {
                        "status": "success",
                        "count": 0,
                        "clubs": [],
                        "message": "모집 중인 동아리가 없습니다",
                    },
                }, 200

            # 모집 중인 동아리가 있는 경우
            return {
                "ok": True,
                "data": {
                    "status": "success",
                    "count": len(clubs_data),
                    "clubs": clubs_data,
                },
            }, 200

        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


# 문항 수정/삭제 엔드포인트
@home_ns.route("/application/questions/<int:question_id>")
class QuestionResource(QuestionController):
    """지원서 문항 수정/삭제 리소스"""

    @home_ns.expect(club_question_update_model)
    def patch(self, question_id):
        """지원서 문항 수정"""
        return super().patch(question_id)

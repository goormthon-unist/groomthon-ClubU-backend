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

club_status_model = home_ns.model(
    "ClubStatus",
    {
        "status": fields.String(
            required=True, description="동아리 모집 상태", enum=["recruiting", "closed"]
        ),
    },
)

club_response_model = home_ns.model(
    "ClubResponse",
    {
        "status": fields.String(description="응답 상태", example="success"),
        "club": fields.Nested(
            home_ns.model(
                "Club",
                {
                    "id": fields.Integer(description="동아리 ID", example=1),
                    "name": fields.String(
                        description="동아리명", example="구름톤 유니브"
                    ),
                    "category_id": fields.Integer(description="카테고리 ID", example=1),
                    "activity_summary": fields.String(
                        description="활동 요약", example="IT 동아리"
                    ),
                    "president_name": fields.String(
                        description="회장명", example="홍길동"
                    ),
                    "contact": fields.String(
                        description="연락처", example="010-1234-5678"
                    ),
                    "recruitment_status": fields.String(
                        description="모집 상태", example="OPEN", enum=["OPEN", "CLOSED"]
                    ),
                    "current_generation": fields.Integer(
                        description="현재 기수", example=1
                    ),
                    "introduction": fields.String(
                        description="소개글", example="동아리 소개글"
                    ),
                    "recruitment_start": fields.String(
                        description="모집 시작일", example="2025-01-01"
                    ),
                    "recruitment_finish": fields.String(
                        description="모집 마감일", example="2025-12-31"
                    ),
                    "logo_image": fields.String(
                        description="로고 이미지 경로",
                        example="/clubs/1/images/logo.webp",
                    ),
                    "introduction_image": fields.String(
                        description="소개 이미지 경로",
                        example="/clubs/1/images/intro.webp",
                    ),
                    "club_room": fields.String(
                        description="동아리실", example="공학관 101호"
                    ),
                    "created_at": fields.String(
                        description="생성일", example="2025-01-01T00:00:00"
                    ),
                    "updated_at": fields.String(
                        description="수정일", example="2025-01-01T12:00:00"
                    ),
                },
            ),
            description="동아리 정보",
        ),
    },
)

error_response_model = home_ns.model(
    "ErrorResponse",
    {
        "message": fields.String(
            description="에러 메시지", example="400-05: 유효하지 않은 모집 상태입니다"
        ),
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

    @home_ns.expect(club_status_model)
    @home_ns.doc("update_club_status")
    @home_ns.response(200, "동아리 상태 변경 성공", club_response_model)
    @home_ns.response(400, "잘못된 요청", error_response_model)
    @home_ns.response(401, "로그인이 필요합니다", error_response_model)
    @home_ns.response(500, "서버 내부 오류", error_response_model)
    def patch(self, club_id):
        """동아리 모집 상태 변경"""
        return super().patch(club_id)


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

"""
지원서 확인 관련 라우트
"""

from flask_restx import Namespace, fields
from controllers.application_check_controller import (
    ClubApplicantsController,
    ApplicationDetailController,
    ClubMemberRegistrationController,
)

# 네임스페이스 등록
application_check_ns = Namespace(
    "application-check", description="지원서 확인 관리 API"
)

# Swagger 모델 정의
applicants_response_model = application_check_ns.model(
    "ApplicantsResponse",
    {
        "status": fields.String(description="응답 상태", example="success"),
        "count": fields.Integer(description="지원자 수", example=1),
        "applicants": fields.List(
            fields.Nested(
                application_check_ns.model(
                    "Applicant",
                    {
                        "application_id": fields.Integer(
                            description="지원서 ID", example=1
                        ),
                        "name": fields.String(
                            description="이름", example="clubstudent"
                        ),
                        "student_id": fields.String(
                            description="학번", example="20000002"
                        ),
                        "phone_number": fields.String(
                            description="전화번호", example="010-0000-0000"
                        ),
                        "gender": fields.String(description="성별", example="MALE"),
                        "department": fields.Raw(description="학과 정보"),
                        "status": fields.String(
                            description="지원서 상태", example="SUBMITTED"
                        ),
                        "submitted_at": fields.String(
                            description="제출일시", example="2025-01-01T12:00:00"
                        ),
                    },
                )
            ),
            description="지원자 목록",
        ),
    },
)


@application_check_ns.route("/applications")
class ClubApplicantsResource(ClubApplicantsController):
    """동아리 지원자 목록 조회 리소스"""

    @application_check_ns.doc("get_club_applicants")
    @application_check_ns.param("club_id", "동아리 ID", type="integer", required=True)
    @application_check_ns.response(
        200, "지원자 목록 조회 성공", applicants_response_model
    )
    @application_check_ns.response(400, "잘못된 요청")
    @application_check_ns.response(401, "로그인이 필요합니다")
    @application_check_ns.response(500, "서버 내부 오류")
    def get(self):
        """특정 동아리의 지원자 목록을 조회합니다"""
        return super().get()


@application_check_ns.route("/applications/<int:application_id>")
class ApplicationDetailResource(ApplicationDetailController):
    """지원서 상세 조회 리소스"""

    pass


@application_check_ns.route("/members")
class ClubMemberRegistrationResource(ClubMemberRegistrationController):
    """동아리원 등록 리소스"""

    def post(self):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404

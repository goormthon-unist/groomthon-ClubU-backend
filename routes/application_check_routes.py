"""
지원서 확인 관련 라우트
"""

from flask_restx import Namespace
from controllers.application_check_controller import (
    ClubApplicantsController,
    ApplicationDetailController,
    ClubMemberRegistrationController,
)

# 네임스페이스 등록
application_check_ns = Namespace("application-check", description="지원서 확인 관리 API")


@application_check_ns.route("/applications")
class ClubApplicantsResource(ClubApplicantsController):
    """동아리 지원자 목록 조회 리소스"""

    pass


@application_check_ns.route("/applications/<int:application_id>")
class ApplicationDetailResource(ApplicationDetailController):
    """지원서 상세 조회 리소스"""

    pass


@application_check_ns.route("/members")
class ClubMemberRegistrationResource(ClubMemberRegistrationController):
    """동아리원 등록 리소스"""

    pass

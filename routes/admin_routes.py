"""
관리자 전용 라우트
"""

from flask_restx import Namespace, Resource
from controllers.admin_controller import (
    AdminClubMemberRegistrationController,
    AdminClubMemberRemovalController,
    AdminRolesController,
    AdminClubMembersController,
    AdminRoleDetailController,
)

# 관리자 전용 네임스페이스
admin_ns = Namespace("admin", description="시스템 관리자 전용 API")


# 동아리원 등록 및 권한 부여
@admin_ns.route("/club-members/register")
class AdminClubMemberRegistrationResource(AdminClubMemberRegistrationController):
    """동아리원 등록 및 권한 부여 리소스 (관리자 전용)"""

    pass


# 동아리원 탈퇴
@admin_ns.route("/club-members/remove")
class AdminClubMemberRemovalResource(AdminClubMemberRemovalController):
    """동아리원 탈퇴 리소스 (관리자 전용)"""

    pass


# 역할 목록 조회
@admin_ns.route("/roles")
class AdminRolesResource(AdminRolesController):
    """역할 목록 조회 리소스 (관리자 전용)"""

    pass


@admin_ns.route("/roles/<int:role_id>")
class AdminRoleDetailResource(AdminRoleDetailController):
    """역할 상세 관리 리소스 (관리자 전용)"""

    pass


# 동아리원 목록 조회
@admin_ns.route("/clubs/<int:club_id>/members")
class AdminClubMembersResource(AdminClubMembersController):
    """동아리원 목록 조회 리소스 (관리자 전용)"""

    pass


# 테스트용 엔드포인트 (권한 확인 없음)
@admin_ns.route("/test")
class AdminTestResource(Resource):
    """관리자 API 테스트용 리소스"""

    def get(self):
        return {"status": "success", "message": "관리자 API 연결 성공!"}

    def post(self):
        return {"status": "success", "message": "POST 요청도 성공!"}

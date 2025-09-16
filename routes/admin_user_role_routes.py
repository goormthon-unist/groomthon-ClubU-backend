"""
관리자용 사용자 권한 변경 라우트
DEVELOPER 권한을 가진 관리자만 접근 가능
"""

from flask_restx import Namespace
from controllers.admin_user_role_controller import (
    AdminUserRoleChangeController,
    AdminUserRolesController,
    AdminAvailableRolesController,
)

# 네임스페이스 등록
admin_user_role_ns = Namespace("admin", description="관리자용 사용자 권한 관리 API")


# API 엔드포인트 등록
@admin_user_role_ns.route("/users/<int:user_id>/roles")
class AdminUserRoleChangeResource(AdminUserRoleChangeController):
    """사용자 권한 변경 리소스"""

    @admin_user_role_ns.doc("change_user_role")
    @admin_user_role_ns.response(200, "권한 변경 성공")
    @admin_user_role_ns.response(400, "잘못된 요청")
    @admin_user_role_ns.response(401, "로그인이 필요합니다")
    @admin_user_role_ns.response(403, "DEVELOPER 권한이 필요합니다")
    @admin_user_role_ns.response(500, "서버 내부 오류")
    def post(self, user_id):
        """
        사용자 권한 변경

        요청 본문:
        {
            "club_id": 1,           // 동아리 ID (선택사항, null이면 전역 권한)
            "role_name": "CLUB_PRESIDENT",  // 새로운 역할명 (필수)
            "generation": 5,        // 기수 (선택사항)
            "other_info": "추가 정보"  // 기타 정보 (선택사항)
        }

        예시:
        - A동아리 멤버를 A동아리 회장으로 변경: {"club_id": 1, "role_name": "CLUB_PRESIDENT"}
        - 전역 관리자 권한 부여: {"club_id": null, "role_name": "UNION_ADMIN"}
        """
        return super().post(user_id)


@admin_user_role_ns.route("/users/<int:user_id>/roles")
class AdminUserRolesResource(AdminUserRolesController):
    """사용자 권한 조회 리소스"""

    @admin_user_role_ns.doc("get_user_roles")
    @admin_user_role_ns.response(200, "권한 조회 성공")
    @admin_user_role_ns.response(400, "잘못된 요청")
    @admin_user_role_ns.response(401, "로그인이 필요합니다")
    @admin_user_role_ns.response(403, "DEVELOPER 권한이 필요합니다")
    @admin_user_role_ns.response(500, "서버 내부 오류")
    def get(self, user_id):
        """
        사용자 권한 조회

        특정 사용자의 모든 권한 정보를 조회합니다.
        """
        return super().get(user_id)


@admin_user_role_ns.route("/roles")
class AdminAvailableRolesResource(AdminAvailableRolesController):
    """사용 가능한 역할 조회 리소스"""

    @admin_user_role_ns.doc("get_available_roles")
    @admin_user_role_ns.response(200, "역할 목록 조회 성공")
    @admin_user_role_ns.response(401, "로그인이 필요합니다")
    @admin_user_role_ns.response(403, "DEVELOPER 권한이 필요합니다")
    @admin_user_role_ns.response(500, "서버 내부 오류")
    def get(self):
        """
        사용 가능한 역할 목록 조회

        시스템에서 사용 가능한 모든 역할 목록을 조회합니다.
        """
        return super().get()

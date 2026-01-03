from flask_restx import Namespace
from controllers.role_controller import (
    RoleListController,
    RoleDetailController,
    ClubMemberRoleController,
    ClubRoleUsersController,
    ClubMembersController,
    CurrentUserPermissionController,
    CurrentUserClubsController,
)

# 네임스페이스 등록
role_ns = Namespace("roles", description="역할 관리 API")


# API 엔드포인트 등록
@role_ns.route("/")
class RoleListResource(RoleListController):
    """역할 목록 조회 리소스"""

    def get(self):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404


@role_ns.route("/<int:role_id>")
class RoleDetailResource(RoleDetailController):
    """역할 상세 조회 리소스"""

    def get(self, role_id):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404


@role_ns.route("/clubs/<int:club_id>/members")
class ClubMembersResource(ClubMembersController):
    """동아리 멤버 목록 조회 리소스"""

    def get(self, club_id):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404


@role_ns.route("/clubs/<int:club_id>/roles/<int:role_id>/users")
class ClubRoleUsersResource(ClubRoleUsersController):
    """동아리에서 역할별 사용자 조회 리소스"""

    def get(self, club_id, role_id):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404


# @role_ns.route("/clubs/<int:club_id>/users/<int:user_id>")
# class ClubMemberRoleResource(ClubMemberRoleController):
#     """동아리 멤버 역할 관리 리소스 (DEPRECATED - use /api/v1/clubs/{club_id}/members/{user_id}/role instead)"""
#     pass


@role_ns.route("/clubs/<int:club_id>/my-permission")
class CurrentUserPermissionResource(CurrentUserPermissionController):
    """현재 사용자 권한 확인 리소스 (쿠키 기반)"""

    def get(self, club_id):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404


@role_ns.route("/my-clubs")
class CurrentUserClubsResource(CurrentUserClubsController):
    """현재 사용자 동아리 목록 조회 리소스 (쿠키 기반)"""

    def get(self):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404

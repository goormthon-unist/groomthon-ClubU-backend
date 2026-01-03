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

    pass


@role_ns.route("/<int:role_id>")
class RoleDetailResource(RoleDetailController):
    """역할 상세 조회 리소스"""

    pass


# @role_ns.route("/clubs/<int:club_id>/users/<int:user_id>")
# class ClubMemberRoleResource(ClubMemberRoleController):
#     """동아리 멤버 역할 관리 리소스 (DEPRECATED - use /api/v1/clubs/{club_id}/members/{user_id}/role instead)"""
#     pass


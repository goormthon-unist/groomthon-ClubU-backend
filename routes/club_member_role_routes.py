"""
동아리 멤버 권한 관리 라우트
동아리 회장이 자신의 동아리 내에서만 멤버 권한을 변경할 수 있도록 제한
"""

from flask_restx import Namespace
from controllers.club_member_role_controller import (
    ClubMemberRoleChangeController,
    ClubMemberRolesController,
    ClubAvailableRolesController,
    ClubMembersListController
)

# 네임스페이스 정의
club_member_role_ns = Namespace(
    "clubs", 
    description="동아리 멤버 권한 관리 API"
)

# 라우트 등록
@club_member_role_ns.route("/<int:club_id>/members/roles")
class ClubMembersListResource(ClubMembersListController):
    pass

@club_member_role_ns.route("/<int:club_id>/members/<int:user_id>/role")
class ClubMemberRoleChangeResource(ClubMemberRoleChangeController):
    pass

@club_member_role_ns.route("/<int:club_id>/members/<int:user_id>/role")
class ClubMemberRolesResource(ClubMemberRolesController):
    pass

@club_member_role_ns.route("/roles")
class ClubAvailableRolesResource(ClubAvailableRolesController):
    pass

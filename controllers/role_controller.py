from flask_restx import Resource, reqparse
from services.role_service import (
    create_role,
    get_all_roles,
    get_role_by_id,
    assign_role_to_user_in_club,
    get_user_role_in_club,
    remove_user_role_from_club,
    get_users_by_role_in_club,
    get_all_club_members,
    check_current_user_permission,
    get_current_user_clubs,
)


class RoleListController(Resource):
    """역할 목록 조회 컨트롤러"""

    def get(self):
        """모든 역할 목록을 반환합니다"""
        try:
            roles_data = get_all_roles()
            return {
                "count": len(roles_data),
                "roles": roles_data,
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class RoleDetailController(Resource):
    """역할 상세 조회 컨트롤러"""

    def get(self, role_id):
        """특정 역할의 상세 정보를 반환합니다"""
        try:
            role_data = get_role_by_id(role_id)
            if not role_data:
                return {
                    "status": "error",
                    "message": "해당 역할을 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return role_data, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class RoleCreateController(Resource):
    """역할 생성 컨트롤러"""

    def post(self):
        """새로운 역할을 생성합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True, location="json")
            parser.add_argument("description", type=str, location="json")
            args = parser.parse_args()

            role_data = create_role(args["name"], args.get("description"))
            return role_data, 201

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMemberRoleController(Resource):
    """동아리 멤버 역할 관리 컨트롤러"""

    def get(self, club_id, user_id):
        """사용자의 특정 동아리에서의 역할을 조회합니다"""
        try:
            role_data = get_user_role_in_club(user_id, club_id)
            if not role_data:
                return {
                    "message": "해당 동아리의 멤버가 아닙니다",
                    "role": None,
                }, 200

            return role_data, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

    def post(self, club_id, user_id):
        """사용자에게 특정 동아리에서 역할을 부여합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("role_id", type=int, required=True, location="json")
            args = parser.parse_args()

            result = assign_role_to_user_in_club(user_id, club_id, args["role_id"])
            return {
                "message": "역할이 성공적으로 부여되었습니다",
                "role": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

    def delete(self, club_id, user_id):
        """사용자의 특정 동아리에서의 역할을 제거합니다"""
        try:
            result = remove_user_role_from_club(user_id, club_id)
            return {
                "message": "역할이 성공적으로 제거되었습니다",
                "result": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-03"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubRoleUsersController(Resource):
    """동아리에서 역할별 사용자 조회 컨트롤러"""

    def get(self, club_id, role_id):
        """특정 동아리에서 특정 역할을 가진 사용자들을 조회합니다"""
        try:
            users_data = get_users_by_role_in_club(club_id, role_id)
            return {
                "count": len(users_data),
                "users": users_data,
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMembersController(Resource):
    """동아리 멤버 목록 조회 컨트롤러"""

    def get(self, club_id):
        """동아리의 모든 멤버를 조회합니다"""
        try:
            members_data = get_all_club_members(club_id)
            return {
                "count": len(members_data),
                "members": members_data,
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-05"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class CurrentUserPermissionController(Resource):
    """현재 사용자 권한 확인 컨트롤러 (쿠키 기반)"""

    def get(self, club_id):
        """쿠키 세션을 통해 현재 사용자의 동아리 권한을 확인합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("required_role", type=str, location="args")
            args = parser.parse_args()

            permission_data = check_current_user_permission(
                club_id, args.get("required_role")
            )

            return permission_data, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class CurrentUserClubsController(Resource):
    """현재 사용자 동아리 목록 조회 컨트롤러 (쿠키 기반)"""

    def get(self):
        """쿠키 세션을 통해 현재 사용자가 속한 모든 동아리를 조회합니다"""
        try:
            clubs_data = get_current_user_clubs()

            return {
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

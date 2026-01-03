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
from utils.permission_decorator import require_permission


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
    """비활성화된 엔드포인트"""

    def get(self, club_id, role_id):
        return {"status": "error", "message": "not found"}, 404


class ClubMembersController(Resource):
    """비활성화된 엔드포인트"""

    def get(self, club_id):
        return {"status": "error", "message": "not found"}, 404


class CurrentUserPermissionController(Resource):
    """비활성화된 엔드포인트"""

    def get(self, club_id):
        return {"status": "error", "message": "not found"}, 404


class CurrentUserClubsController(Resource):
    """비활성화된 엔드포인트"""

    def get(self):
        return {"status": "error", "message": "not found"}, 404

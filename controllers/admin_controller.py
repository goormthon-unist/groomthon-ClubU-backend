"""
관리자 전용 컨트롤러
"""

from flask import request
from flask_restx import Resource, abort, reqparse
from services.admin_service import (
    register_club_member_admin,
    remove_club_member_admin,
    get_available_roles,
    get_club_members_admin,
    create_role,
    update_role,
    delete_role,
)


class AdminClubMemberRegistrationController(Resource):
    """관리자 동아리원 등록 및 권한 부여 컨트롤러"""

    def post(self):
        """동아리원 등록 및 권한 부여 (관리자 전용)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "user_id",
                type=int,
                required=True,
                location="json",
                help="사용자 ID가 필요합니다",
            )
            parser.add_argument(
                "club_id",
                type=int,
                required=True,
                location="json",
                help="동아리 ID가 필요합니다",
            )
            parser.add_argument(
                "role_id",
                type=int,
                required=True,
                location="json",
                help="역할 ID가 필요합니다",
            )
            parser.add_argument(
                "generation",
                type=int,
                location="json",
                help="기수 (선택사항)",
            )
            parser.add_argument(
                "other_info",
                type=str,
                location="json",
                help="기타 정보 (선택사항)",
            )

            args = parser.parse_args()

            result = register_club_member_admin(
                user_id=args["user_id"],
                club_id=args["club_id"],
                role_id=args["role_id"],
                generation=args.get("generation"),
                other_info=args.get("other_info"),
            )

            return {"status": "success", **result}, 201

        except ValueError as e:
            abort(400, f"400-20: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class AdminClubMemberRemovalController(Resource):
    """관리자 동아리원 탈퇴 컨트롤러"""

    def delete(self):
        """동아리원 탈퇴 (관리자 전용)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "user_id",
                type=int,
                required=True,
                location="json",
                help="사용자 ID가 필요합니다",
            )
            parser.add_argument(
                "club_id",
                type=int,
                required=True,
                location="json",
                help="동아리 ID가 필요합니다",
            )

            args = parser.parse_args()

            result = remove_club_member_admin(
                user_id=args["user_id"],
                club_id=args["club_id"],
            )

            return {"status": "success", **result}, 200

        except ValueError as e:
            abort(400, f"400-21: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class AdminRolesController(Resource):
    """관리자 역할 관리 컨트롤러"""

    def get(self):
        """사용 가능한 역할 목록 조회 (관리자 전용)"""
        try:
            roles = get_available_roles()
            return {
                "status": "success",
                "count": len(roles),
                "roles": roles,
            }, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def post(self):
        """역할 생성 (관리자 전용)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "role_name",
                type=str,
                required=True,
                location="json",
                help="역할명이 필요합니다",
            )
            args = parser.parse_args()

            role = create_role(args["role_name"])
            return {"status": "success", "role": role}, 201

        except ValueError as e:
            abort(400, f"400-23: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class AdminRoleDetailController(Resource):
    """관리자 역할 상세 관리 컨트롤러"""

    def patch(self, role_id):
        """역할명 수정 (관리자 전용)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "role_name",
                type=str,
                required=True,
                location="json",
                help="역할명이 필요합니다",
            )
            args = parser.parse_args()

            role = update_role(role_id, args["role_name"])
            return {"status": "success", "role": role}, 200

        except ValueError as e:
            abort(400, f"400-24: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def delete(self, role_id):
        """역할 삭제 (관리자 전용)"""
        try:
            result = delete_role(role_id)
            return {"status": "success", **result}, 200

        except ValueError as e:
            abort(400, f"400-25: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class AdminClubMembersController(Resource):
    """관리자 동아리원 목록 조회 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 동아리원 목록 조회 (관리자 전용)"""
        try:
            members = get_club_members_admin(club_id)
            return {
                "status": "success",
                "count": len(members),
                "members": members,
            }, 200

        except ValueError as e:
            abort(400, f"400-22: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

"""
동아리 멤버 권한 관리 컨트롤러
동아리 회장이 자신의 동아리 내에서만 멤버 권한을 변경할 수 있도록 제한
"""

from flask_restx import Resource, reqparse
from flask import request, current_app
from services.club_member_role_service import (
    register_club_member_improved,
    change_club_member_role,
    get_club_member_roles,
    get_club_available_roles,
    get_club_members_list,
)
from utils.permission_decorator import require_permission


class ClubMemberRegistrationController(Resource):
    """동아리 멤버 직접 등록 컨트롤러"""

    @require_permission("clubs.member_role_change", club_id_param="club_id")
    def post(self, club_id):
        """
        개선된 동아리 멤버 등록 (학번과 이름으로 검색)

        Args:
            club_id: 동아리 ID

        Body:
            {
                "student_id": "20240001",
                "name": "김지원",
                "role_name": "CLUB_MEMBER" | "CLUB_OFFICER" | "CLUB_PRESIDENT" | "CLUB_MEMBER_REST" | "STUDENT",
                "generation": 1,  // 선택사항
                "other_info": "기타 정보"  // 선택사항
            }
        """
        try:
            # JSON 파싱
            data = request.get_json()
            if not data:
                return {
                    "status": "error",
                    "message": "요청 본문이 필요합니다",
                    "code": "400-00",
                }, 400

            # 필수 필드 검증
            student_id = data.get("student_id")
            name = data.get("name")
            role_name = data.get("role_name")

            if not student_id:
                return {
                    "status": "error",
                    "message": "학번이 필요합니다",
                    "code": "400-01",
                }, 400
            if not name:
                return {
                    "status": "error",
                    "message": "이름이 필요합니다",
                    "code": "400-02",
                }, 400
            if not role_name:
                return {
                    "status": "error",
                    "message": "역할 이름이 필요합니다",
                    "code": "400-03",
                }, 400

            # 선택 필드
            generation = data.get("generation")
            other_info = data.get("other_info")

            # 개선된 동아리 멤버 등록 실행
            result = register_club_member_improved(
                club_id=club_id,
                student_id=student_id,
                name=name,
                role_name=role_name,
                generation=generation,
                other_info=other_info,
            )

            if result["success"]:
                return {
                    "message": result["message"],
                    "member": result["data"],
                }, 201
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "code": "400-00",
                }, 400

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            current_app.logger.exception("club.member_registration failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMemberRoleChangeController(Resource):
    """동아리 멤버 권한 변경 컨트롤러"""

    @require_permission("clubs.member_role_change", club_id_param="club_id")
    def post(self, club_id, user_id):
        """
        동아리 멤버 권한 변경

        Args:
            club_id: 동아리 ID
            user_id: 사용자 ID

        Body:
            {
                "role_name": "CLUB_MEMBER" | "CLUB_OFFICER" | "CLUB_PRESIDENT",
                "generation": 1,  // 선택사항
                "other_info": "기타 정보"  // 선택사항
            }
        """
        try:
            # JSON 파싱
            data = request.get_json()
            if not data:
                return {
                    "status": "error",
                    "message": "요청 본문이 필요합니다",
                    "code": "400-00",
                }, 400

            # 필수 필드 검증
            role_name = data.get("role_name")
            if not role_name:
                return {
                    "status": "error",
                    "message": "역할 이름이 필요합니다",
                    "code": "400-01",
                }, 400

            # 선택 필드
            generation = data.get("generation")
            other_info = data.get("other_info")

            # 권한 변경 실행
            result = change_club_member_role(
                club_id=club_id,
                user_id=user_id,
                role_name=role_name,
                generation=generation,
                other_info=other_info,
            )

            if result["success"]:
                return {
                    "message": result["message"],
                    "member": result["data"],
                }, 200
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "code": "400-00",
                }, 400

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            current_app.logger.exception("club.member_role_change failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMemberRolesController(Resource):
    """동아리 멤버 권한 조회 컨트롤러"""

    @require_permission("clubs.member_roles_list", club_id_param="club_id")
    def get(self, club_id, user_id):
        """
        동아리 내 특정 사용자의 역할 조회

        Args:
            club_id: 동아리 ID
            user_id: 사용자 ID
        """
        try:
            # 권한 조회 실행
            result = get_club_member_roles(club_id=club_id, user_id=user_id)

            if result["success"]:
                return {
                    "message": result["message"],
                    "roles": result["data"],
                }, 200
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "code": "400-00",
                }, 400

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            current_app.logger.exception("club.member_roles_list failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubAvailableRolesController(Resource):
    """동아리 내 사용 가능한 역할 목록 조회 컨트롤러"""

    @require_permission("clubs.member_roles_list")
    def get(self):
        """
        동아리 내에서 사용 가능한 역할 목록 조회
        """
        try:
            # 역할 목록 조회 실행
            result = get_club_available_roles()

            if result["success"]:
                return {
                    "message": result["message"],
                    "roles": result["data"],
                }, 200
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "code": "400-00",
                }, 400

        except Exception as e:
            current_app.logger.exception("club.available_roles failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMembersListController(Resource):
    """동아리 멤버 목록 조회 컨트롤러"""

    @require_permission("clubs.members_list", club_id_param="club_id")
    def get(self, club_id):
        """
        동아리 멤버 목록 조회 (권한별 정렬)

        Args:
            club_id: 동아리 ID
        """
        try:
            # 멤버 목록 조회 실행
            result = get_club_members_list(club_id=club_id)

            if result["success"]:
                return {
                    "message": result["message"],
                    "members": result["data"],
                }, 200
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "code": "400-00",
                }, 400

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            current_app.logger.exception("club.members_list failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

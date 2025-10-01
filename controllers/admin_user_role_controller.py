"""
관리자용 사용자 권한 변경 컨트롤러
DEVELOPER 권한을 가진 관리자만 접근 가능
"""

from flask import request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest, HTTPException

from services.admin_user_role_service import (
    change_user_role,
    get_user_roles,
    get_available_roles,
)
from utils.permission_decorator import require_permission


class AdminUserRoleChangeController(Resource):
    """사용자 권한 변경 컨트롤러"""

    @require_permission("admin.user_role_change")
    def post(self, user_id):
        """사용자 권한 변경 API"""
        try:
            # 1) JSON 파싱
            try:
                data = request.get_json(force=False, silent=False)
            except BadRequest:
                return {
                    "status": "error",
                    "message": "유효하지 않은 JSON 형식입니다",
                    "code": "400-00",
                }, 400

            if not isinstance(data, dict):
                return {
                    "status": "error",
                    "message": "JSON 객체가 필요합니다",
                    "code": "400-00",
                }, 400

            # 2) 필드 추출/검증
            club_id = data.get("club_id")  # None 허용 (전역 권한)
            new_role_name = (data.get("role_name") or "").strip()
            generation = data.get("generation")
            other_info = data.get("other_info")

            if not new_role_name:
                return {
                    "status": "error",
                    "message": "역할 이름이 필요합니다",
                    "code": "400-01",
                }, 400

            # club_id가 제공된 경우 정수로 변환
            if club_id is not None:
                try:
                    club_id = int(club_id)
                except (ValueError, TypeError):
                    return {
                        "status": "error",
                        "message": "동아리 ID는 정수여야 합니다",
                        "code": "400-02",
                    }, 400

            # generation이 제공된 경우 정수로 변환
            if generation is not None:
                try:
                    generation = int(generation)
                except (ValueError, TypeError):
                    return {
                        "status": "error",
                        "message": "기수는 정수여야 합니다",
                        "code": "400-03",
                    }, 400

            # 3) 사용자 ID 검증
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                return {
                    "status": "error",
                    "message": "사용자 ID는 정수여야 합니다",
                    "code": "400-04",
                }, 400

            # 4) 권한 변경 실행
            result = change_user_role(
                user_id=user_id,
                club_id=club_id,
                new_role_name=new_role_name,
                generation=generation,
                other_info=other_info,
            )

            return {
                "message": result["message"],
                "user_role": result["data"],
            }, 200

        except ValueError as ve:
            return {"status": "error", "message": str(ve), "code": "400-05"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class AdminUserRolesController(Resource):
    """사용자 권한 조회 컨트롤러"""

    @require_permission("admin.user_role_change")
    def get(self, user_id):
        """사용자 권한 조회 API"""
        try:
            # 1) 사용자 ID 검증
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                return {
                    "status": "error",
                    "message": "사용자 ID는 정수여야 합니다",
                    "code": "400-01",
                }, 400

            # 2) 사용자 권한 조회
            result = get_user_roles(user_id=user_id)

            return {
                "message": "사용자 권한 조회가 완료되었습니다",
                "roles": result["data"],
            }, 200

        except ValueError as ve:
            return {"status": "error", "message": str(ve), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class AdminAvailableRolesController(Resource):
    """사용 가능한 역할 조회 컨트롤러"""

    @require_permission("admin.user_role_change")
    def get(self):
        """사용 가능한 역할 목록 조회 API"""
        try:
            # 사용 가능한 역할 조회
            result = get_available_roles()

            return {
                "message": "사용 가능한 역할 목록 조회가 완료되었습니다",
                "roles": result["data"],
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

from flask_restx import Resource
from flask import session
from services.session_service import get_current_session
from services.user_service import (
    get_user_profile,
    get_user_clubs,
    get_user_submitted_applications,
)


class UserProfileController(Resource):
    """사용자 프로필 조회 컨트롤러 (마이페이지용)"""

    def get(self):
        """현재 사용자의 프로필 정보를 반환합니다"""
        try:
            # 현재 세션 정보 조회
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            user_id = session_data["user_id"]

            user_data = get_user_profile(user_id)
            if not user_data:
                return {
                    "status": "error",
                    "message": "해당 사용자를 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return user_data, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class UserClubsController(Resource):
    """사용자가 속한 동아리 목록 조회 컨트롤러"""

    def get(self):
        """현재 사용자가 속한 동아리 목록을 반환합니다"""
        try:
            # 현재 세션 정보 조회
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            user_id = session_data["user_id"]

            clubs_data = get_user_clubs(user_id)

            return {
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class UserApplicationsController(Resource):
    """사용자가 지원한 동아리 지원서 목록 조회 컨트롤러 (SUBMITTED 상태만)"""

    def get(self):
        """현재 사용자가 지원한 동아리 지원서 목록을 반환합니다"""
        try:
            # 현재 세션 정보 조회
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            user_id = session_data["user_id"]

            applications_data = get_user_submitted_applications(user_id)

            return {
                "count": len(applications_data),
                "applications": applications_data,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-03"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

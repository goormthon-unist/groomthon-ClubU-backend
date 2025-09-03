from flask_restx import Resource, abort
from flask import session
from werkzeug.exceptions import HTTPException
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
                abort(401, "401-01: 로그인이 필요합니다")

            user_id = session_data["user_id"]

            user_data = get_user_profile(user_id)
            if not user_data:
                abort(404, "404-01: 해당 사용자를 찾을 수 없습니다")

            return {
                "ok": True,
                "data": {"status": "success", "user": user_data},
            }, 200

        except HTTPException as he:
            raise he
        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class UserClubsController(Resource):
    """사용자가 속한 동아리 목록 조회 컨트롤러"""

    def get(self):
        """현재 사용자가 속한 동아리 목록을 반환합니다"""
        try:
            # 현재 세션 정보 조회
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            user_id = session_data["user_id"]

            clubs_data = get_user_clubs(user_id)

            return {
                "ok": True,
                "data": {
                    "status": "success",
                    "count": len(clubs_data),
                    "clubs": clubs_data,
                },
            }, 200

        except HTTPException as he:
            raise he
        except ValueError as e:
            abort(400, f"400-02: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class UserApplicationsController(Resource):
    """사용자가 지원한 동아리 지원서 목록 조회 컨트롤러 (SUBMITTED 상태만)"""

    def get(self):
        """현재 사용자가 지원한 동아리 지원서 목록을 반환합니다"""
        try:
            # 현재 세션 정보 조회
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            user_id = session_data["user_id"]

            applications_data = get_user_submitted_applications(user_id)

            return {
                "ok": True,
                "data": {
                    "status": "success",
                    "count": len(applications_data),
                    "applications": applications_data,
                },
            }, 200

        except HTTPException as he:
            raise he
        except ValueError as e:
            abort(400, f"400-03: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

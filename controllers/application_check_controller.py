"""
지원서 확인 관련 컨트롤러
"""

from flask import request
from flask_restx import Resource
from services.session_service import get_current_session
from services.application_check_service import (
    get_club_applicants,
    get_application_detail,
    register_club_member,
)


class ClubApplicantsController(Resource):
    """동아리 지원자 목록 조회 컨트롤러"""

    def get(self):
        """특정 동아리의 지원자 목록을 조회합니다"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 쿼리 파라미터에서 club_id 가져오기
            club_id = request.args.get("club_id", type=int)
            if not club_id:
                return {
                    "status": "error",
                    "message": "club_id 파라미터가 필요합니다",
                    "code": "400-12",
                }, 400

            applicants = get_club_applicants(club_id)
            return {
                "count": len(applicants),
                "applicants": applicants,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-12"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ApplicationDetailController(Resource):
    """지원서 상세 조회 컨트롤러"""

    def get(self, application_id):
        """특정 지원서의 상세 정보를 조회합니다"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            application_detail = get_application_detail(application_id)
            return application_detail, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-13"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMemberRegistrationController(Resource):
    """동아리원 등록 컨트롤러"""

    def post(self):
        """비활성화된 엔드포인트"""
        return {"status": "error", "message": "not found"}, 404

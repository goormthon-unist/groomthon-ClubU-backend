"""
지원서 확인 관련 컨트롤러
"""

from flask import request
from flask_restx import Resource, abort
from services.application_check_service import (
    get_club_applicants,
    get_application_detail,
    register_club_member
)


class ClubApplicantsController(Resource):
    """동아리 지원자 목록 조회 컨트롤러"""

    def get(self):
        """특정 동아리의 지원자 목록을 조회합니다"""
        try:
            # 쿼리 파라미터에서 club_id 가져오기
            club_id = request.args.get('club_id', type=int)
            if not club_id:
                abort(400, "400-12: club_id 파라미터가 필요합니다")
            
            applicants = get_club_applicants(club_id)
            return {
                "status": "success",
                "count": len(applicants),
                "applicants": applicants
            }, 200

        except ValueError as e:
            abort(400, f"400-12: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ApplicationDetailController(Resource):
    """지원서 상세 조회 컨트롤러"""

    def get(self, application_id):
        """특정 지원서의 상세 정보를 조회합니다"""
        try:
            application_detail = get_application_detail(application_id)
            return {
                "status": "success",
                "application": application_detail
            }, 200

        except ValueError as e:
            abort(400, f"400-13: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubMemberRegistrationController(Resource):
    """동아리원 등록 컨트롤러"""

    def post(self):
        """지원자를 동아리원으로 등록합니다"""
        try:
            # 구현 예정 - Mock 응답
            return {
                "status": "success",
                "message": "동아리원 등록 기능 구현 예정"
            }, 200

        except ValueError as e:
            abort(400, f"400-14: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

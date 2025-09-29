"""
사용자 검색 컨트롤러
학번과 이름으로 사용자를 검증하는 API
"""

from flask_restx import Resource, abort
from flask import request, current_app
from services.user_search_service import find_user_by_student_id_and_name
from services.session_service import get_current_user


class UserValidationController(Resource):
    """사용자 검증 컨트롤러"""

    def post(self):
        """
        학번과 이름으로 사용자 검증

        Body:
            {
                "student_id": "20240001",
                "name": "김지원"
            }
        """
        try:
            # 로그인 체크
            current_user = get_current_user()
            if not current_user:
                abort(401, "401-01: 로그인이 필요합니다")

            # JSON 파싱
            data = request.get_json()
            if not data:
                abort(400, "400-00: JSON body is required")

            # 필수 필드 검증
            student_id = data.get("student_id")
            name = data.get("name")

            if not student_id:
                abort(400, "400-01: student_id is required")
            if not name:
                abort(400, "400-02: name is required")

            # 사용자 검증 실행
            result = find_user_by_student_id_and_name(student_id, name)

            return {
                "status": "success",
                "message": "사용자 정보가 확인되었습니다.",
                "data": result,
            }, 200

        except ValueError as e:
            abort(400, f"400-03: {str(e)}")
        except Exception as e:
            current_app.logger.exception("user.validation failed")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

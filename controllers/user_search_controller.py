"""
사용자 검색 컨트롤러
학번과 이름으로 사용자를 검증하는 API
"""

from flask_restx import Resource


class UserValidationController(Resource):
    """비활성화된 엔드포인트"""

    def post(self):
        """비활성화된 엔드포인트 (미사용)"""
        return {"status": "error", "message": "not found"}, 404

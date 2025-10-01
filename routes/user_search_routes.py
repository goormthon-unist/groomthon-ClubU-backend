"""
사용자 검색 라우트
학번과 이름으로 사용자를 검증하는 API
"""

from flask_restx import Namespace, fields
from controllers.user_search_controller import UserValidationController

# 네임스페이스 정의
user_search_ns = Namespace("users", description="사용자 검색 API")

# Request Body 모델 정의
user_validation_model = user_search_ns.model(
    "UserValidation",
    {
        "student_id": fields.String(required=True, description="학번"),
        "name": fields.String(required=True, description="이름"),
    },
)


# API 엔드포인트 등록
@user_search_ns.route("/validate")
class UserValidationResource(UserValidationController):
    """사용자 검증 리소스"""

    @user_search_ns.doc("validate_user")
    @user_search_ns.expect(user_validation_model)
    @user_search_ns.response(200, "사용자 검증 성공")
    @user_search_ns.response(400, "잘못된 요청")
    @user_search_ns.response(401, "로그인이 필요합니다")
    @user_search_ns.response(500, "서버 내부 오류")
    def post(self):
        """
        학번과 이름으로 사용자 검증

        요청 본문:
        {
            "student_id": "20240001",
            "name": "김지원"
        }

        응답:
        {
            "message": "사용자 정보가 확인되었습니다.",
            "user": {
                "success": true,
                "user_id": 123,
                "name": "김지원",
                "student_id": "20240001",
                "email": "jiwon.kim@unist.ac.kr",
                "department": {
                    "id": 1,
                    "name": "컴퓨터공학과"
                }
            }
        }
        """
        return super().post()

from flask_restx import Resource
from services.session_service import get_current_session
from services.notice_asset_service import delete_notice_asset_by_id
from services.club_info_service import check_club_president_permission
from utils.permission_decorator import require_permission


class NoticeAssetController(Resource):
    """공지사항 첨부파일 개별 관리 컨트롤러"""

    def delete(self, notice_id, asset_id):
        """개별 첨부파일 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 공지사항 작성자 권한 확인
            user_id = session_data["user_id"]

            # 첨부파일 삭제
            result = delete_notice_asset_by_id(asset_id)

            return {
                "message": "첨부파일이 성공적으로 삭제되었습니다",
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

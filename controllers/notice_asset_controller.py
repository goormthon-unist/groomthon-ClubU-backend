from flask_restx import Resource
from services.session_service import get_current_session
from services.notice_asset_service import delete_notice_asset_by_id
from services.club_info_service import check_club_president_permission
from utils.permission_decorator import require_permission


class NoticeAssetController(Resource):
    """공지사항 첨부파일 개별 관리 컨트롤러"""

    def delete(self, notice_id, asset_id):
        """개별 첨부파일 삭제"""
        """비활성화된 엔드포인트 (미사용)"""
        return {"status": "error", "message": "not found"}, 404

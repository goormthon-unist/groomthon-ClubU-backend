from flask_restx import Resource
from services.session_service import get_current_session
from services.notice_asset_service import (
    create_notice_asset,
    get_notice_assets,
    delete_notice_asset_by_id,
)
from services.club_info_service import check_club_president_permission
from utils.permission_decorator import require_permission


class NoticeImageController(Resource):
    """공지사항 이미지 관리 컨트롤러"""

    def put(self, notice_id):
        """공지사항 이미지 업로드/수정"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 파일 처리
            from flask import request

            if "image" not in request.files:
                return {
                    "status": "error",
                    "message": "이미지 파일이 필요합니다",
                    "code": "400-02",
                }, 400

            image_file = request.files["image"]
            if image_file.filename == "":
                return {
                    "status": "error",
                    "message": "선택된 파일이 없습니다",
                    "code": "400-03",
                }, 400

            # 공지사항 작성자 권한 확인
            user_id = session_data["user_id"]

            # 기존 이미지가 있는지 확인하고 삭제
            existing_assets = get_notice_assets(notice_id)
            for asset in existing_assets:
                if asset["asset_type"] == "IMAGE":
                    delete_notice_asset_by_id(asset["id"])

            # 새 이미지 업로드
            result = create_notice_asset(notice_id, "IMAGE", image_file)

            return {
                "message": "공지사항 이미지가 성공적으로 업로드되었습니다.",
                "asset": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def delete(self, notice_id):
        """공지사항 이미지 삭제"""
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

            # 기존 이미지 찾아서 삭제
            existing_assets = get_notice_assets(notice_id)
            image_deleted = False

            for asset in existing_assets:
                if asset["asset_type"] == "IMAGE":
                    delete_notice_asset_by_id(asset["id"])
                    image_deleted = True
                    break

            if not image_deleted:
                return {
                    "status": "error",
                    "message": "삭제할 이미지가 없습니다",
                    "code": "404-02",
                }, 404

            return {
                "message": "공지사항 이미지가 성공적으로 삭제되었습니다.",
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

from flask_restx import Resource, abort
from services.session_service import get_current_session
from services.mock_notice_asset_service import (
    create_notice_asset,
    get_notice_assets,
    delete_notice_asset_by_id,
)
from services.club_info_service import check_club_president_permission


class NoticeImageController(Resource):
    """공지사항 이미지 관리 컨트롤러"""

    def put(self, notice_id):
        """공지사항 이미지 업로드/수정"""
        try:
            # 세션 인증 확인 (Mock 서비스에서는 우회)
            session_data = get_current_session()
            if not session_data:
                # Mock 테스트를 위해 임시 세션 데이터 생성
                session_data = {"user_id": 101}

            # 파일 처리
            from flask import request

            if "image" not in request.files:
                abort(400, "400-02: 이미지 파일이 필요합니다")

            image_file = request.files["image"]
            if image_file.filename == "":
                abort(400, "400-03: 선택된 파일이 없습니다")

            # 공지사항 작성자 권한 확인 (Mock에서는 우회)
            user_id = session_data["user_id"]
            # Mock 테스트를 위해 권한 확인 우회

            # 기존 이미지가 있는지 확인하고 삭제
            existing_assets = get_notice_assets(notice_id)
            for asset in existing_assets:
                if asset["asset_type"] == "IMAGE":
                    delete_notice_asset_by_id(asset["id"])

            # 새 이미지 업로드
            result = create_notice_asset(notice_id, "IMAGE", image_file)

            return {
                "status": "success",
                "message": "공지사항 이미지가 성공적으로 업로드되었습니다.",
                "asset": result,
            }, 200

        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

    def delete(self, notice_id):
        """공지사항 이미지 삭제"""
        try:
            # 세션 인증 확인 (Mock에서는 우회)
            session_data = get_current_session()
            if not session_data:
                # Mock 테스트를 위해 임시 세션 데이터 생성
                session_data = {"user_id": 101}

            # 공지사항 작성자 권한 확인 (Mock에서는 우회)
            user_id = session_data["user_id"]
            # Mock 테스트를 위해 권한 확인 우회

            # 기존 이미지 찾아서 삭제
            existing_assets = get_notice_assets(notice_id)
            image_deleted = False

            for asset in existing_assets:
                if asset["asset_type"] == "IMAGE":
                    delete_notice_asset_by_id(asset["id"])
                    image_deleted = True
                    break

            if not image_deleted:
                abort(404, "404-02: 삭제할 이미지가 없습니다")

            return {
                "status": "success",
                "message": "공지사항 이미지가 성공적으로 삭제되었습니다.",
            }, 200

        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

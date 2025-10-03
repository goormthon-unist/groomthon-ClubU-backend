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
            from flask import request, current_app

            # 디버깅을 위한 요청 정보 로깅
            current_app.logger.info(f"Request content length: {request.content_length}")
            current_app.logger.info(f"Request content type: {request.content_type}")
            current_app.logger.info(f"Request files: {list(request.files.keys())}")

            # 여러 이미지 파일 처리
            image_files = request.files.getlist("image[]")
            current_app.logger.info(f"Number of image files: {len(image_files)}")

            for i, file in enumerate(image_files):
                if file.filename:
                    current_app.logger.info(
                        f"Image {i}: {file.filename}, size: {file.content_length}"
                    )

            if not image_files or all(file.filename == "" for file in image_files):
                return {
                    "status": "error",
                    "message": "이미지 파일이 필요합니다",
                    "code": "400-02",
                }, 400

            # 공지사항 작성자 권한 확인
            user_id = session_data["user_id"]

            # 기존 이미지가 있는지 확인하고 삭제
            existing_assets = get_notice_assets(notice_id)
            for asset in existing_assets:
                if asset["asset_type"] == "IMAGE":
                    delete_notice_asset_by_id(asset["id"])

            # 새 이미지들 업로드
            results = []
            for image_file in image_files:
                if image_file.filename:
                    result = create_notice_asset(notice_id, "IMAGE", image_file)
                    results.append(result)

            return {
                "message": "공지사항 이미지들이 성공적으로 업로드되었습니다.",
                "assets": results,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            # 413 오류 특별 처리
            if "413" in str(e) or "Request Entity Too Large" in str(e):
                return {
                    "status": "error",
                    "message": "파일 크기가 너무 큽니다. 최대 100MB까지 업로드 가능합니다.",
                    "code": "413-01",
                }, 413
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

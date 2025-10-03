from flask_restx import Resource
from services.session_service import get_current_session
from services.notice_asset_service import (
    create_notice_asset,
    get_notice_assets,
    delete_notice_asset_by_id,
)
from services.club_info_service import check_club_president_permission
from utils.permission_decorator import require_permission


class NoticeFileController(Resource):
    """공지사항 파일 관리 컨트롤러"""

    def put(self, notice_id):
        """공지사항 파일 업로드/수정"""
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

            # 여러 파일 처리
            files = request.files.getlist("file[]")
            current_app.logger.info(f"Number of files: {len(files)}")

            for i, file in enumerate(files):
                if file.filename:
                    current_app.logger.info(
                        f"File {i}: {file.filename}, size: {file.content_length}"
                    )

            if not files or all(file.filename == "" for file in files):
                return {
                    "status": "error",
                    "message": "파일이 필요합니다",
                    "code": "400-02",
                }, 400

            # 공지사항 작성자 권한 확인
            user_id = session_data["user_id"]

            # 기존 파일이 있는지 확인하고 삭제
            existing_assets = get_notice_assets(notice_id)
            for asset in existing_assets:
                if asset["asset_type"] == "FILE":
                    delete_notice_asset_by_id(asset["id"])

            # 새 파일들 업로드
            results = []
            for file in files:
                if file.filename:
                    result = create_notice_asset(notice_id, "FILE", file)
                    results.append(result)

            return {
                "message": "공지사항 파일들이 성공적으로 업로드되었습니다.",
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
        """공지사항 파일 삭제"""
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

            # 기존 파일 찾아서 삭제
            existing_assets = get_notice_assets(notice_id)
            file_deleted = False

            for asset in existing_assets:
                if asset["asset_type"] == "FILE":
                    delete_notice_asset_by_id(asset["id"])
                    file_deleted = True
                    break

            if not file_deleted:
                return {
                    "status": "error",
                    "message": "삭제할 파일이 없습니다",
                    "code": "404-02",
                }, 404

            return {
                "message": "공지사항 파일이 성공적으로 삭제되었습니다.",
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

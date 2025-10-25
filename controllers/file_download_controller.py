from flask import send_file, abort, current_app
from flask_restx import Resource
from services.session_service import get_current_session
from services.notice_asset_service import get_notice_asset_by_id
import os


class FileDownloadController(Resource):
    """파일 다운로드 컨트롤러"""

    def get(self, asset_id):
        """파일 다운로드"""
        try:
            # 공지사항 첨부파일은 누구나 다운로드 가능 (인증 제거)

            # 첨부파일 정보 조회
            asset = get_notice_asset_by_id(asset_id)
            if not asset:
                return {
                    "status": "error",
                    "message": "파일을 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            # 파일 경로 확인 (절대 경로로 변환)
            relative_path = asset.get("file_path")
            if not relative_path:
                return {
                    "status": "error",
                    "message": "파일 경로를 찾을 수 없습니다",
                    "code": "404-02",
                }, 404

            # 절대 경로로 변환
            from flask import current_app

            # relative_path가 이미 notices/로 시작하므로 그대로 사용
            file_path = relative_path

            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"파일이 존재하지 않습니다: {file_path}",
                    "code": "404-02",
                }, 404

            # 파일명 추출 (원본 파일명 사용)
            original_filename = asset.get("original_filename", "download")

            # 파일 다운로드
            return send_file(
                file_path,
                as_attachment=True,
                download_name=original_filename,
                mimetype="application/octet-stream",
            )

        except Exception as e:
            current_app.logger.error(f"파일 다운로드 중 오류: {e}")
            return {
                "status": "error",
                "message": f"파일 다운로드 중 오류가 발생했습니다: {e}",
                "code": "500-01",
            }, 500

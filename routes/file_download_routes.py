from flask_restx import Namespace, Resource
from controllers.file_download_controller import FileDownloadController

# 네임스페이스 생성
file_download_ns = Namespace(
    "file-download",
    description="파일 다운로드 API",
    path="/api/v1",
)


# 라우트 등록
@file_download_ns.route("/download/<int:asset_id>")
class FileDownloadResource(FileDownloadController):
    """파일 다운로드 리소스"""

    @file_download_ns.doc("download_file")
    @file_download_ns.response(200, "파일 다운로드 성공")
    @file_download_ns.response(401, "로그인이 필요합니다")
    @file_download_ns.response(404, "파일을 찾을 수 없습니다")
    @file_download_ns.response(500, "서버 내부 오류")
    def get(self, asset_id):
        """
        파일 다운로드

        첨부파일 ID를 통해 파일을 다운로드합니다.
        """
        return super().get(asset_id)

from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from controllers.notice_image_controller import NoticeImageController
from controllers.notice_file_controller import NoticeFileController

# 네임스페이스 생성
notice_asset_ns = Namespace(
    "notice-assets",
    description="공지사항 첨부파일 관리 API",
    path="/api/v1/notices",
)

# RequestParser 정의 (파일 업로드용)
image_parser = reqparse.RequestParser()
image_parser.add_argument(
    "image",
    type=FileStorage,
    location="files",
    required=True,
    help="공지사항 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)",
)

file_parser = reqparse.RequestParser()
file_parser.add_argument(
    "file",
    type=FileStorage,
    location="files",
    required=True,
    help="공지사항 파일 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)",
)


# 라우트 등록
@notice_asset_ns.route("/<int:notice_id>/image")
class NoticeImageResource(NoticeImageController):
    """공지사항 이미지 관리 리소스"""

    @notice_asset_ns.expect(image_parser)
    @notice_asset_ns.doc("upload_notice_image", consumes=["multipart/form-data"])
    @notice_asset_ns.response(200, "이미지 업로드 성공")
    @notice_asset_ns.response(400, "잘못된 요청")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def put(self, notice_id):
        """
        공지사항 이미지 업로드/수정

        multipart/form-data로 요청:
        - image: 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)
        """
        return super().put(notice_id)

    @notice_asset_ns.doc("delete_notice_image")
    @notice_asset_ns.response(200, "이미지 삭제 성공")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @notice_asset_ns.response(404, "이미지를 찾을 수 없습니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def delete(self, notice_id):
        """공지사항 이미지 삭제"""
        return super().delete(notice_id)


@notice_asset_ns.route("/<int:notice_id>/files")
class NoticeFileResource(NoticeFileController):
    """공지사항 파일 관리 리소스"""

    @notice_asset_ns.expect(file_parser)
    @notice_asset_ns.doc("upload_notice_file", consumes=["multipart/form-data"])
    @notice_asset_ns.response(200, "파일 업로드 성공")
    @notice_asset_ns.response(400, "잘못된 요청")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def put(self, notice_id):
        """
        공지사항 파일 업로드/수정

        multipart/form-data로 요청:
        - file: 문서 파일 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)
        """
        return super().put(notice_id)

    @notice_asset_ns.doc("delete_notice_file")
    @notice_asset_ns.response(200, "파일 삭제 성공")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @notice_asset_ns.response(404, "파일을 찾을 수 없습니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def delete(self, notice_id):
        """공지사항 파일 삭제"""
        return super().delete(notice_id)

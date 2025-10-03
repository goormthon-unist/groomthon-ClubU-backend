from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from controllers.notice_image_controller import NoticeImageController
from controllers.notice_file_controller import NoticeFileController
from controllers.notice_asset_controller import NoticeAssetController

# 네임스페이스 생성
notice_asset_ns = Namespace(
    "notice-assets",
    description="공지사항 첨부파일 관리 API",
    path="/api/v1/notices",
)

# RequestParser 정의 (파일 업로드용) - 단일/다중 파일 모두 지원
image_parser = reqparse.RequestParser()
image_parser.add_argument(
    "images",
    type=FileStorage,
    location="files",
    action="append",
    required=False,
    help="공지사항 이미지 파일들 (PNG, JPG, JPEG, GIF, BMP)",
)
image_parser.add_argument(
    "image",
    type=FileStorage,
    location="files",
    required=False,
    help="공지사항 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)",
)

file_parser = reqparse.RequestParser()
file_parser.add_argument(
    "files",
    type=FileStorage,
    location="files",
    action="append",
    required=False,
    help="공지사항 파일들 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)",
)
file_parser.add_argument(
    "file",
    type=FileStorage,
    location="files",
    required=False,
    help="공지사항 파일 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)",
)


# 라우트 등록
@notice_asset_ns.route("/<int:notice_id>/image")
class NoticeImageResource(NoticeImageController):
    """공지사항 이미지 관리 리소스"""

    @notice_asset_ns.expect(image_parser)
    @notice_asset_ns.doc("upload_notice_images", consumes=["multipart/form-data"])
    @notice_asset_ns.response(200, "이미지들 업로드 성공")
    @notice_asset_ns.response(400, "잘못된 요청")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def post(self, notice_id):
        """
        공지사항 이미지 업로드 (단일/다중 지원)

        multipart/form-data로 요청:
        - image: 단일 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)
        - images: 여러 이미지 파일들 (PNG, JPG, JPEG, GIF, BMP)
        """
        return super().post(notice_id)

    @notice_asset_ns.doc("delete_notice_image")
    @notice_asset_ns.response(200, "이미지 삭제 성공")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(404, "이미지를 찾을 수 없습니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def delete(self, notice_id):
        """공지사항 이미지 삭제"""
        return super().delete(notice_id)


@notice_asset_ns.route("/<int:notice_id>/files")
class NoticeFileResource(NoticeFileController):
    """공지사항 파일 관리 리소스"""

    @notice_asset_ns.expect(file_parser)
    @notice_asset_ns.doc("upload_notice_files", consumes=["multipart/form-data"])
    @notice_asset_ns.response(200, "파일들 업로드 성공")
    @notice_asset_ns.response(400, "잘못된 요청")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def post(self, notice_id):
        """
        공지사항 파일 업로드 (단일/다중 지원)

        multipart/form-data로 요청:
        - file: 단일 파일 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)
        - files: 여러 파일들 (DOC, DOCX, XLS, XLSX, PPT, PPTX, HWP, HWPX, PDF, TXT, RTF, ZIP, RAR, 7Z)
        """
        return super().post(notice_id)

    @notice_asset_ns.doc("delete_notice_file")
    @notice_asset_ns.response(200, "파일 삭제 성공")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(404, "파일을 찾을 수 없습니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def delete(self, notice_id):
        """공지사항 파일 삭제"""
        return super().delete(notice_id)


# 개별 첨부파일 삭제 라우트
@notice_asset_ns.route("/<int:notice_id>/assets/<int:asset_id>")
class NoticeAssetResource(NoticeAssetController):
    """공지사항 개별 첨부파일 관리 리소스"""

    @notice_asset_ns.doc("delete_notice_asset")
    @notice_asset_ns.response(200, "첨부파일 삭제 성공")
    @notice_asset_ns.response(401, "로그인이 필요합니다")
    @notice_asset_ns.response(404, "첨부파일을 찾을 수 없습니다")
    @notice_asset_ns.response(500, "서버 내부 오류")
    def delete(self, notice_id, asset_id):
        """개별 첨부파일 삭제"""
        return super().delete(notice_id, asset_id)

from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage
from controllers.banner_controller import (
    BannerController,
    BannerDetailController,
    BannerStatusController,
)

# 네임스페이스 등록
banner_ns = Namespace("banners", description="배너 관리 API")

# RequestParser 정의 (배너 이미지 업로드용)
banner_parser = reqparse.RequestParser()
banner_parser.add_argument(
    "club_id", type=int, location="form", required=True, help="동아리 ID"
)
banner_parser.add_argument(
    "title", type=str, location="form", required=True, help="배너 제목"
)
banner_parser.add_argument("description", type=str, location="form", help="배너 설명")
banner_parser.add_argument(
    "position", type=str, location="form", help="배너 위치 (TOP, BOTTOM)"
)
banner_parser.add_argument(
    "start_date",
    type=str,
    location="form",
    required=True,
    help="시작 날짜 (YYYY-MM-DD)",
)
banner_parser.add_argument(
    "end_date", type=str, location="form", required=True, help="종료 날짜 (YYYY-MM-DD)"
)
banner_parser.add_argument(
    "image", type=FileStorage, location="files", required=True, help="배너 이미지 파일"
)

banner_status_model = banner_ns.model(
    "BannerStatus",
    {
        "status": fields.String(
            required=True, description="배너 상태 (WAITING, REJECTED, POSTED, ARCHIVED)"
        )
    },
)


# 배너 관리 엔드포인트
@banner_ns.route("/")
class BannerResource(BannerController):
    """배너 관리 리소스"""

    @banner_ns.expect(banner_parser)
    @banner_ns.doc("create_banner", consumes=["multipart/form-data"])
    def post(self):
        """배너 등록"""
        return super().post()


@banner_ns.route("/<int:banner_id>")
class BannerDetailResource(BannerDetailController):
    """배너 상세 관리 리소스"""

    pass


@banner_ns.route("/<int:banner_id>/status")
class BannerStatusResource(BannerStatusController):
    """배너 상태 관리 리소스"""

    @banner_ns.expect(banner_status_model)
    def patch(self, banner_id):
        """배너 상태 변경"""
        return super().patch(banner_id)

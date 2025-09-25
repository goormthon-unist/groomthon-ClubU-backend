from flask_restx import Namespace, fields
from controllers.banner_controller import (
    BannerController,
    BannerDetailController,
    BannerStatusController,
)

# 네임스페이스 등록
banner_ns = Namespace("banners", description="배너 관리 API")

# Swagger 모델 정의
banner_create_model = banner_ns.model(
    "BannerCreate",
    {
        "club_id": fields.Integer(required=True, description="동아리 ID"),
        "title": fields.String(required=True, description="배너 제목"),
        "description": fields.String(description="배너 설명"),
        "position": fields.String(description="배너 위치 (TOP, BOTTOM)", default="TOP"),
        "start_date": fields.String(
            required=True, description="시작 날짜 (YYYY-MM-DD)"
        ),
        "end_date": fields.String(required=True, description="종료 날짜 (YYYY-MM-DD)"),
        "image": fields.Raw(required=True, description="배너 이미지 파일"),
    },
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
@banner_ns.route("/banners/")
class BannerResource(BannerController):
    """배너 관리 리소스"""

    @banner_ns.expect(banner_create_model)
    def post(self):
        """배너 등록"""
        return super().post()


@banner_ns.route("/banners/<int:banner_id>")
class BannerDetailResource(BannerDetailController):
    """배너 상세 관리 리소스"""

    pass


@banner_ns.route("/banners/<int:banner_id>/status")
class BannerStatusResource(BannerStatusController):
    """배너 상태 관리 리소스"""

    @banner_ns.expect(banner_status_model)
    def patch(self, banner_id):
        """배너 상태 변경"""
        return super().patch(banner_id)

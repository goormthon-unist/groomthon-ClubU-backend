from flask_restx import Namespace
from controllers.banner_controller import (
    BannerController,
    BannerDetailController,
    BannerStatusController,
)

# 네임스페이스 등록
banner_ns = Namespace("banners", description="배너 관리 API")


# 배너 관리 엔드포인트
@banner_ns.route("/banners/")
class BannerResource(BannerController):
    """배너 관리 리소스"""

    pass


@banner_ns.route("/banners/<int:banner_id>")
class BannerDetailResource(BannerDetailController):
    """배너 상세 관리 리소스"""

    pass


@banner_ns.route("/banners/<int:banner_id>/status")
class BannerStatusResource(BannerStatusController):
    """배너 상태 관리 리소스"""

    pass

from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage
from controllers.banner_controller import (
    BannerController,
    BannerDetailController,
    BannerStatusController,
    BannerAllController,
    BannerClubsController,
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

# 응답 모델 정의
banner_model = banner_ns.model(
    "Banner",
    {
        "id": fields.Integer(description="배너 ID"),
        "club_id": fields.Integer(description="동아리 ID"),
        "user_id": fields.Integer(description="사용자 ID"),
        "club_name": fields.String(description="동아리명"),
        "file_path": fields.String(description="이미지 파일 경로"),
        "clublogoImageUrl": fields.String(description="동아리 로고 이미지 URL"),
        "position": fields.String(description="배너 위치", enum=["TOP", "BOTTOM"]),
        "status": fields.String(
            description="배너 상태", enum=["WAITING", "REJECTED", "POSTED", "ARCHIVED"]
        ),
        "uploaded_at": fields.String(description="업로드 시간"),
        "start_date": fields.String(description="시작 날짜"),
        "end_date": fields.String(description="종료 날짜"),
        "title": fields.String(description="배너 제목"),
        "description": fields.String(description="배너 설명"),
    },
)

banner_list_model = banner_ns.model(
    "BannerList",
    {
        "status": fields.String(description="응답 상태"),
        "count": fields.Integer(description="배너 개수"),
        "banners": fields.List(fields.Nested(banner_model), description="배너 목록"),
    },
)

banner_response_model = banner_ns.model(
    "BannerResponse",
    {
        "status": fields.String(description="응답 상태"),
        "banner": fields.Nested(banner_model, description="배너 정보"),
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

banner_status_response_model = banner_ns.model(
    "BannerStatusResponse",
    {
        "status": fields.String(description="응답 상태"),
        "banner": fields.Nested(banner_model, description="배너 정보"),
    },
)

banner_delete_response_model = banner_ns.model(
    "BannerDeleteResponse",
    {
        "status": fields.String(description="응답 상태"),
        "message": fields.String(description="삭제 결과 메시지"),
    },
)

banner_clubs_response_model = banner_ns.model(
    "BannerClubsResponse",
    {
        "status": fields.String(description="응답 상태"),
        "data": fields.Raw(description="동아리 ID를 키로 하는 객체, 각 값은 배너 배열"),
        "count": fields.Raw(
            description="동아리 ID를 키로 하는 객체, 각 값은 배너 개수"
        ),
    },
)


# 배너 관리 엔드포인트
@banner_ns.route("/")
class BannerResource(BannerController):
    """배너 관리 리소스"""

    @banner_ns.doc(
        "create_banner", consumes=["multipart/form-data"], security="sessionAuth"
    )
    @banner_ns.expect(banner_parser)
    @banner_ns.response(201, "배너 등록 성공", banner_response_model)
    @banner_ns.response(400, "잘못된 요청")
    @banner_ns.response(401, "로그인이 필요합니다")
    @banner_ns.response(500, "서버 내부 오류")
    def post(self):
        """배너 등록"""
        return super().post()

    @banner_ns.doc("get_banners")
    @banner_ns.response(200, "배너 목록 조회 성공 (POSTED만)", banner_list_model)
    @banner_ns.response(500, "서버 내부 오류")
    def get(self):
        """배너 목록 조회 (POSTED 상태만 반환)"""
        return super().get()


@banner_ns.route("/all")
class BannerAllResource(BannerAllController):
    """전체 배너 목록 조회 리소스 (관리자용)"""

    @banner_ns.doc("get_all_banners")
    @banner_ns.response(200, "전체 배너 목록 조회 성공", banner_list_model)
    @banner_ns.response(401, "로그인이 필요합니다")
    @banner_ns.response(403, "UNION_ADMIN 또는 DEVELOPER 권한이 필요합니다")
    @banner_ns.response(500, "서버 내부 오류")
    def get(self):
        """전체 배너 목록 조회 (관리자 및 동연회 권한 필요)"""
        return super().get()


@banner_ns.route("/clubs")
class BannerClubsResource(BannerClubsController):
    """동아리별 배너 목록 조회 리소스"""

    @banner_ns.doc("get_banners_by_clubs", security="sessionAuth")
    @banner_ns.param(
        "club_ids",
        "동아리 ID 배열 (쉼표로 구분된 문자열)",
        required=True,
        type="string",
        example="1,2,3",
    )
    @banner_ns.response(
        200, "동아리별 배너 목록 조회 성공", banner_clubs_response_model
    )
    @banner_ns.response(400, "잘못된 요청")
    @banner_ns.response(401, "로그인이 필요합니다")
    @banner_ns.response(500, "서버 내부 오류")
    def get(self):
        """동아리별 배너 목록 조회 (CLUB_PRESIDENT, UNION_ADMIN, DEVELOPER 권한 필요)"""
        return super().get()


@banner_ns.route("/<int:banner_id>")
class BannerDetailResource(BannerDetailController):
    """배너 상세 관리 리소스"""

    @banner_ns.doc("get_banner_detail")
    @banner_ns.response(200, "배너 상세 조회 성공", banner_response_model)
    @banner_ns.response(404, "해당 배너를 찾을 수 없습니다")
    @banner_ns.response(500, "서버 내부 오류")
    def get(self, banner_id):
        """배너 상세 조회"""
        return super().get(banner_id)

    @banner_ns.doc("delete_banner")
    @banner_ns.response(200, "배너 삭제 성공", banner_delete_response_model)
    @banner_ns.response(400, "잘못된 요청")
    @banner_ns.response(401, "로그인이 필요합니다")
    @banner_ns.response(404, "해당 배너를 찾을 수 없습니다")
    @banner_ns.response(500, "서버 내부 오류")
    def delete(self, banner_id):
        """배너 삭제"""
        return super().delete(banner_id)


@banner_ns.route("/<int:banner_id>/status")
class BannerStatusResource(BannerStatusController):
    """배너 상태 관리 리소스"""

    @banner_ns.doc("update_banner_status")
    @banner_ns.expect(banner_status_model)
    @banner_ns.response(200, "배너 상태 변경 성공", banner_status_response_model)
    @banner_ns.response(400, "잘못된 요청")
    @banner_ns.response(401, "로그인이 필요합니다")
    @banner_ns.response(404, "해당 배너를 찾을 수 없습니다")
    @banner_ns.response(500, "서버 내부 오류")
    def patch(self, banner_id):
        """배너 상태 변경"""
        return super().patch(banner_id)

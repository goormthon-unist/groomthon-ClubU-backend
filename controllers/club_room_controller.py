from flask import request
from flask_restx import Resource, Namespace
from services.club_room_service import ClubRoomService
from utils.permission_decorator import require_permission

club_room_ns = Namespace("clubs", description="동아리 공간 관리 API")


@club_room_ns.route("/<int:club_id>/remaining-usage")
class ClubRemainingUsageController(Resource):
    @club_room_ns.doc("get_club_remaining_usage")
    @club_room_ns.param("date", "조회할 날짜 (YYYY-MM-DD)", required=True)
    @club_room_ns.response(200, "성공")
    @club_room_ns.response(400, "잘못된 요청")
    @club_room_ns.response(404, "동아리를 찾을 수 없음")
    @club_room_ns.response(500, "서버 오류")
    @require_permission("clubs.remaining_usage", club_id_param="club_id")
    def get(self, club_id):
        """동아리별 사용 가능 시간 조회"""
        try:
            date = request.args.get("date")
            if not date:
                return {
                    "status": "error",
                    "message": "날짜 파라미터가 필요합니다.",
                }, 400

            usage_info = ClubRoomService.get_club_remaining_usage(club_id, date)
            return {
                "status": "success",
                "data": usage_info,
                "message": "동아리 사용 가능 시간 조회 성공",
            }, 200
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e),
            }, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"사용 가능 시간 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500

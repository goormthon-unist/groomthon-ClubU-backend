from flask import request
from flask_restx import Resource, Namespace
from services.room_service import RoomService
from utils.permission_decorator import require_permission

room_ns = Namespace("rooms", description="공간 관리 API")


@room_ns.route("")
class RoomListController(Resource):
    @room_ns.doc("get_all_rooms")
    @room_ns.response(200, "성공")
    @room_ns.response(500, "서버 오류")
    def get(self):
        """전체 공간 조회"""
        try:
            rooms = RoomService.get_all_rooms()
            return {
                "status": "success",
                "data": rooms,
                "message": "전체 공간 조회 성공",
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"공간 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500


@room_ns.route("/<int:room_id>/availability")
class RoomAvailabilityController(Resource):
    @room_ns.doc("get_room_availability")
    @room_ns.param("date", "조회할 날짜 (YYYY-MM-DD)", required=True)
    @room_ns.response(200, "성공")
    @room_ns.response(400, "잘못된 요청")
    @room_ns.response(404, "공간을 찾을 수 없음")
    @room_ns.response(500, "서버 오류")
    @require_permission("rooms.availability")
    def get(self, room_id):
        """공간별 가용시간 조회"""
        try:
            date = request.args.get("date")
            if not date:
                return {
                    "status": "error",
                    "message": "날짜 파라미터가 필요합니다.",
                }, 400

            availability = RoomService.get_room_availability(room_id, date)
            return {
                "status": "success",
                "data": availability,
                "message": "공간 가용시간 조회 성공",
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"가용시간 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500



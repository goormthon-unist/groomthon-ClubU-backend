from flask import request
from flask_restx import Resource, Namespace
from services.reservation_service import ReservationService
from services.session_service import get_session_info
from utils.permission_decorator import require_permission
from models import UserSession

reservation_ns = Namespace("reservations", description="예약 관리 API")


@reservation_ns.route("")
class ReservationController(Resource):
    @reservation_ns.doc("create_reservation")
    @reservation_ns.response(201, "예약 생성 성공")
    @reservation_ns.response(400, "잘못된 요청")
    @reservation_ns.response(500, "서버 오류")
    @require_permission("reservations.create")
    def post(self):
        """동아리별 대관 신청"""
        try:
            data = request.get_json()

            # 필수 필드 검증
            required_fields = [
                "club_id",
                "user_id",
                "room_id",
                "date",
                "start_time",
                "end_time",
            ]
            for field in required_fields:
                if field not in data:
                    return {
                        "status": "error",
                        "message": f"필수 필드 '{field}'가 누락되었습니다.",
                    }, 400

            # 보안 검증: 세션 정보와 요청 데이터 일치 확인
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            # 세션의 사용자 ID와 요청의 user_id 일치 확인
            session_user_id = session_info["user"]["user_id"]
            if session_user_id != data["user_id"]:
                return {
                    "status": "error",
                    "message": "세션의 사용자와 요청한 사용자가 일치하지 않습니다.",
                }, 403

            # 세션의 동아리 멤버십과 요청의 club_id 일치 확인
            user_club_ids = [club["club_id"] for club in session_info["clubs"]]
            if data["club_id"] not in user_club_ids:
                return {
                    "status": "error",
                    "message": "해당 동아리의 멤버가 아닙니다.",
                }, 403

            reservation = ReservationService.create_reservation(
                club_id=data["club_id"],
                user_id=data["user_id"],
                room_id=data["room_id"],
                date=data["date"],
                start_time=data["start_time"],
                end_time=data["end_time"],
                note=data.get("note"),
            )

            return {
                "status": "success",
                "data": reservation,
                "message": "대관 신청이 성공적으로 완료되었습니다.",
            }, 201
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"예약 생성 중 오류가 발생했습니다: {str(e)}",
            }, 500

    @reservation_ns.doc("get_user_reservations")
    @reservation_ns.param(
        "mine", "내 예약만 조회 (true/false)", type=bool, default=True
    )
    @reservation_ns.param(
        "status", "상태 필터 (CONFIRMED,CLEANING_REQUIRED,CLEANING_DONE)", type=str
    )
    @reservation_ns.response(200, "성공")
    @reservation_ns.response(400, "잘못된 요청")
    @reservation_ns.response(500, "서버 오류")
    @require_permission("reservations.list")
    def get(self):
        """사용자(나, 동아리) 대관 신청 목록 조회"""
        try:
            mine = request.args.get("mine", "true").lower() == "true"
            status_filter = request.args.get("status")

            if status_filter:
                status_filter = [s.strip() for s in status_filter.split(",")]

            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            reservations = ReservationService.get_user_reservations(
                user_id=user_id, mine=mine, status_filter=status_filter
            )

            return {
                "status": "success",
                "data": reservations,
                "message": "예약 목록 조회 성공",
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"예약 목록 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500


@reservation_ns.route("/<int:reservation_id>")
class ReservationDetailController(Resource):
    @reservation_ns.doc("get_reservation_detail")
    @reservation_ns.response(200, "성공")
    @reservation_ns.response(404, "예약을 찾을 수 없음")
    @reservation_ns.response(500, "서버 오류")
    @require_permission("reservations.detail")
    def get(self, reservation_id):
        """예약 상세 조회"""
        try:
            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            reservation = ReservationService.get_reservation_detail(reservation_id, user_id)
            return {
                "status": "success",
                "data": reservation,
                "message": "예약 상세 조회 성공",
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 404
        except Exception as e:
            return {
                "status": "error",
                "message": f"예약 상세 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500

    @reservation_ns.doc("cancel_reservation")
    @reservation_ns.response(200, "예약 취소 성공")
    @reservation_ns.response(400, "잘못된 요청")
    @reservation_ns.response(404, "예약을 찾을 수 없음")
    @reservation_ns.response(500, "서버 오류")
    @require_permission("reservations.cancel")
    def delete(self, reservation_id):
        """예약 취소"""
        try:
            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            result = ReservationService.cancel_reservation(reservation_id, user_id)
            return {
                "status": "success",
                "data": result,
                "message": "예약이 성공적으로 취소되었습니다.",
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"예약 취소 중 오류가 발생했습니다: {str(e)}",
            }, 500

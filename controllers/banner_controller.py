from flask_restx import Resource, reqparse
from services.session_service import get_current_session
from services.banner_service import (
    create_banner,
    delete_banner,
    get_banner_by_id,
    get_banners,
    get_all_banners,
    update_banner_status,
)
from utils.permission_decorator import require_permission


class BannerController(Resource):
    """배너 관리 컨트롤러"""

    def post(self):
        """배너 등록"""
        try:
            from flask import current_app, request

            # 디버깅을 위한 세션 정보 로깅
            current_app.logger.info("=== Banner POST Request Debug ===")
            current_app.logger.info(f"Request headers: {dict(request.headers)}")
            current_app.logger.info(f"Request cookies: {dict(request.cookies)}")

            # 세션 인증 확인
            session_data = get_current_session()
            current_app.logger.info(f"Session data: {session_data}")

            if not session_data:
                current_app.logger.warning("No session data found - returning 401")
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # multipart/form-data와 JSON 모두 처리
            from flask import request

            # form-data에서 데이터 파싱 (multipart/form-data)
            parser = reqparse.RequestParser()
            parser.add_argument("club_id", type=int, required=True, location="form")
            parser.add_argument("title", type=str, required=True, location="form")
            parser.add_argument("description", type=str, location="form")
            parser.add_argument("position", type=str, location="form")
            parser.add_argument("start_date", type=str, required=True, location="form")
            parser.add_argument("end_date", type=str, required=True, location="form")

            try:
                args = parser.parse_args()
            except Exception:
                # JSON으로 시도
                data = request.get_json()
                if not data:
                    return {
                        "status": "error",
                        "message": "요청 데이터가 필요합니다",
                        "code": "400-01",
                    }, 400
                args = data

            # 파일 처리
            if "image" not in request.files:
                return {
                    "status": "error",
                    "message": "이미지 파일이 필요합니다",
                    "code": "400-02",
                }, 400

            image_file = request.files["image"]
            if image_file.filename == "":
                return {
                    "status": "error",
                    "message": "선택된 파일이 없습니다",
                    "code": "400-03",
                }, 400

            # 필수 필드 검증
            club_id = args.get("club_id")
            title = args.get("title")
            start_date = args.get("start_date")
            end_date = args.get("end_date")

            if not club_id:
                return {
                    "status": "error",
                    "message": "club_id가 필요합니다",
                    "code": "400-04",
                }, 400
            if not title:
                return {
                    "status": "error",
                    "message": "title이 필요합니다",
                    "code": "400-05",
                }, 400
            if not start_date:
                return {
                    "status": "error",
                    "message": "start_date가 필요합니다",
                    "code": "400-06",
                }, 400
            if not end_date:
                return {
                    "status": "error",
                    "message": "end_date가 필요합니다",
                    "code": "400-07",
                }, 400

            banner_data = {
                "title": title,
                "description": args.get("description", ""),
                "position": args.get("position", "TOP"),
                "start_date": start_date,
                "end_date": end_date,
            }

            # 세션에서 user_id 가져오기
            user_id = session_data["user_id"]
            new_banner = create_banner(club_id, user_id, banner_data, image_file)
            return new_banner, 201

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-08"}, 400
        except Exception as e:
            from flask import current_app

            current_app.logger.exception("Banner creation failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def get(self):
        """배너 목록 조회 (POSTED 상태만 반환)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("position", type=str, location="args")
            args = parser.parse_args()

            banners = get_banners(position=args.get("position"))

            return {
                "count": len(banners),
                "banners": banners,
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class BannerDetailController(Resource):
    """배너 상세 관리 컨트롤러"""

    def get(self, banner_id):
        """배너 상세 조회"""
        try:
            banner = get_banner_by_id(banner_id)
            if not banner:
                return {
                    "status": "error",
                    "message": "해당 배너를 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return banner, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def delete(self, banner_id):
        """배너 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            result = delete_banner(banner_id)
            return {"message": result["message"]}, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class BannerAllController(Resource):
    """전체 배너 목록 조회 컨트롤러 (관리자용)"""

    @require_permission("banners.list_all")
    def get(self):
        """전체 배너 목록 조회 (관리자 및 동연회 권한 필요)"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, location="args")
            parser.add_argument("position", type=str, location="args")
            args = parser.parse_args()

            banners = get_all_banners(
                status=args.get("status"), position=args.get("position")
            )

            return {
                "count": len(banners),
                "banners": banners,
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class BannerStatusController(Resource):
    """배너 상태 관리 컨트롤러"""

    def patch(self, banner_id):
        """배너 상태 변경"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, required=True, location="json")
            args = parser.parse_args()

            banner = update_banner_status(banner_id, args["status"])
            return banner, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-05"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

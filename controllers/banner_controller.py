from flask_restx import Resource, abort, reqparse
from services.session_service import get_current_session
from services.banner_service import (
    create_banner,
    delete_banner,
    get_banner_by_id,
    get_banners,
    update_banner_status,
)


class BannerController(Resource):
    """배너 관리 컨트롤러"""

    def post(self):
        """배너 등록"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

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
                    abort(400, "400-01: 요청 데이터가 필요합니다")
                args = data

            # 파일 처리
            if "image" not in request.files:
                abort(400, "400-02: 이미지 파일이 필요합니다")

            image_file = request.files["image"]
            if image_file.filename == "":
                abort(400, "400-03: 선택된 파일이 없습니다")

            # 필수 필드 검증
            club_id = args.get("club_id")
            title = args.get("title")
            start_date = args.get("start_date")
            end_date = args.get("end_date")

            if not club_id:
                abort(400, "400-04: club_id가 필요합니다")
            if not title:
                abort(400, "400-05: title이 필요합니다")
            if not start_date:
                abort(400, "400-06: start_date가 필요합니다")
            if not end_date:
                abort(400, "400-07: end_date가 필요합니다")

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
            return {"status": "success", "banner": new_banner}, 201

        except ValueError as e:
            abort(400, f"400-08: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

    def get(self):
        """배너 목록 조회"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, location="args")
            parser.add_argument("position", type=str, location="args")
            args = parser.parse_args()

            banners = get_banners(
                status=args.get("status"), position=args.get("position")
            )

            return {
                "status": "success",
                "count": len(banners),
                "banners": banners,
            }, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")


class BannerDetailController(Resource):
    """배너 상세 관리 컨트롤러"""

    def get(self, banner_id):
        """배너 상세 조회"""
        try:
            banner = get_banner_by_id(banner_id)
            if not banner:
                abort(404, "404-01: 해당 배너를 찾을 수 없습니다")

            return {"status": "success", "banner": banner}, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

    def delete(self, banner_id):
        """배너 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            result = delete_banner(banner_id)
            return {"status": "success", "message": result["message"]}, 200

        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")


class BannerStatusController(Resource):
    """배너 상태 관리 컨트롤러"""

    def patch(self, banner_id):
        """배너 상태 변경"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, required=True, location="json")
            args = parser.parse_args()

            banner = update_banner_status(banner_id, args["status"])
            return {"status": "success", "banner": banner}, 200

        except ValueError as e:
            abort(400, f"400-05: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

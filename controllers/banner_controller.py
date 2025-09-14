from flask_restx import Resource, abort, reqparse
from services.banner_service import (
    create_banner,
    get_banners,
    get_banner_by_id,
    update_banner_status,
    delete_banner,
)


class BannerController(Resource):
    """배너 관리 컨트롤러"""

    def post(self):
        """배너 등록"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("club_id", type=int, required=True, location="form")
            parser.add_argument("title", type=str, required=True, location="form")
            parser.add_argument("description", type=str, location="form")
            parser.add_argument("location", type=str, location="form")
            parser.add_argument("start_date", type=str, location="form")
            parser.add_argument("end_date", type=str, location="form")
            args = parser.parse_args()

            # 파일 처리
            from flask import request

            if "image" not in request.files:
                abort(400, "400-01: 이미지 파일이 필요합니다")

            image_file = request.files["image"]
            if image_file.filename == "":
                abort(400, "400-02: 선택된 파일이 없습니다")

            banner_data = {
                "title": args["title"],
                "description": args.get("description", ""),
                "location": args.get("location", "MAIN_TOP"),
                "start_date": args.get("start_date"),
                "end_date": args.get("end_date"),
            }

            new_banner = create_banner(args["club_id"], banner_data, image_file)
            return {"status": "success", "banner": new_banner}, 201

        except ValueError as e:
            abort(400, f"400-03: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def get(self):
        """배너 목록 조회"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, location="args")
            parser.add_argument("location", type=str, location="args")
            args = parser.parse_args()

            banners = get_banners(
                status=args.get("status"), location=args.get("location")
            )

            return {"status": "success", "count": len(banners), "banners": banners}, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


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
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def delete(self, banner_id):
        """배너 삭제"""
        try:
            result = delete_banner(banner_id)
            return {"status": "success", "message": result["message"]}, 200

        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class BannerStatusController(Resource):
    """배너 상태 관리 컨트롤러"""

    def patch(self, banner_id):
        """배너 상태 변경"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, required=True, location="json")
            args = parser.parse_args()

            banner = update_banner_status(banner_id, args["status"])
            return {"status": "success", "banner": banner}, 200

        except ValueError as e:
            abort(400, f"400-05: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

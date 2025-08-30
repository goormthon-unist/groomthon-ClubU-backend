from flask_restx import Resource, abort
from services.home_service import get_all_clubs, get_club_by_id, get_open_clubs


class ClubListController(Resource):
    """동아리 목록 조회 컨트롤러"""

    def get(self):
        """모든 동아리 목록을 반환합니다"""
        try:
            clubs_data = get_all_clubs()
            return {
                "status": "success",
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200
        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubDetailController(Resource):
    """동아리 상세 정보 조회 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 상세 정보를 반환합니다"""
        try:
            club_data = get_club_by_id(club_id)
            if not club_data:
                abort(404, "404-01: 해당 동아리를 찾을 수 없습니다")

            return {"status": "success", "club": club_data}, 200
        except ValueError as e:
            abort(400, f"400-02: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class OpenClubsController(Resource):
    """모집 중인 동아리 조회 컨트롤러"""

    def get(self):
        """모집 중인 동아리 목록을 반환합니다"""
        try:
            open_clubs_data = get_open_clubs()
            return {
                "status": "success",
                "count": len(open_clubs_data),
                "clubs": open_clubs_data,
            }, 200
        except ValueError as e:
            # 모집 중인 동아리가 없는 경우 빈 배열과 메시지 반환
            return {
                "status": "success",
                "count": 0,
                "clubs": [],
                "message": str(e),
            }, 200
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

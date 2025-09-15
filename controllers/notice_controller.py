from flask_restx import Resource, abort, reqparse
from services.session_service import get_current_session
from services.notice_service import (
    create_notice,
    delete_notice,
    get_all_notices,
    get_club_notices,
    get_notice_by_id,
    update_notice,
)


class ClubNoticeController(Resource):
    """동아리 공지 관리 컨트롤러"""

    def post(self, club_id):
        """동아리 공지 등록"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, required=True, location="json")
            parser.add_argument("content", type=str, required=True, location="json")
            parser.add_argument("is_important", type=bool, location="json")
            args = parser.parse_args()

            notice_data = {
                "title": args["title"],
                "content": args["content"],
                "is_important": args.get("is_important", False),
            }

            # 세션에서 user_id 가져오기
            user_id = session_data["user_id"]
            new_notice = create_notice(club_id, user_id, notice_data)
            return {"status": "success", "notice": new_notice}, 201

        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

    def get(self, club_id):
        """특정 동아리 공지 목록 조회"""
        try:
            notices = get_club_notices(club_id)
            return {
                "status": "success",
                "count": len(notices),
                "notices": notices,
            }, 200

        except ValueError as e:
            abort(400, f"400-02: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")


class NoticeController(Resource):
    """공지 관리 컨트롤러"""

    def get(self):
        """전체 공지 목록 조회"""
        try:
            notices = get_all_notices()
            return {
                "status": "success",
                "count": len(notices),
                "notices": notices,
            }, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")


class NoticeDetailController(Resource):
    """공지 상세 관리 컨트롤러"""

    def get(self, notice_id):
        """공지 상세 조회"""
        try:
            notice = get_notice_by_id(notice_id)
            if not notice:
                abort(404, "404-01: 해당 공지를 찾을 수 없습니다")

            return {"status": "success", "notice": notice}, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")


class ClubNoticeDetailController(Resource):
    """동아리 공지 상세 관리 컨트롤러"""

    def patch(self, club_id, notice_id):
        """동아리 공지 수정"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, location="json")
            parser.add_argument("content", type=str, location="json")
            parser.add_argument("is_important", type=bool, location="json")
            args = parser.parse_args()

            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                abort(400, "400-03: 수정할 데이터가 없습니다")

            notice = update_notice(notice_id, update_data)
            return {"status": "success", "notice": notice}, 200

        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

    def delete(self, club_id, notice_id):
        """동아리 공지 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                abort(401, "401-01: 로그인이 필요합니다")

            result = delete_notice(notice_id)
            return {"status": "success", "message": result["message"]}, 200

        except ValueError as e:
            abort(400, f"400-05: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {e}")

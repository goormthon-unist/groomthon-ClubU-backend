from flask_restx import Resource, reqparse
from services.session_service import get_current_session
from services.notice_service import (
    create_notice,
    delete_notice,
    get_all_notices,
    get_club_notices,
    get_notice_by_id,
    update_notice,
)
from utils.permission_decorator import require_permission


class ClubNoticeController(Resource):
    """동아리 공지 관리 컨트롤러"""

    @require_permission("notices.club_create", club_id_param="club_id")
    def post(self, club_id):
        """동아리 공지 등록"""
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
            return new_notice, 201

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def get(self, club_id):
        """특정 동아리 공지 목록 조회"""
        try:
            notices = get_club_notices(club_id)
            return {
                "count": len(notices),
                "notices": notices,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class NoticeController(Resource):
    """공지 관리 컨트롤러"""

    def get(self):
        """전체 공지 목록 조회"""
        try:
            notices = get_all_notices()
            return {
                "count": len(notices),
                "notices": notices,
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class NoticeDetailController(Resource):
    """공지 상세 관리 컨트롤러"""

    def get(self, notice_id):
        """공지 상세 조회"""
        try:
            notice = get_notice_by_id(notice_id)
            if not notice:
                return {
                    "status": "error",
                    "message": "해당 공지를 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return notice, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class ClubNoticeDetailController(Resource):
    """동아리 공지 상세 관리 컨트롤러"""

    @require_permission("notices.club_update", club_id_param="club_id")
    def patch(self, club_id, notice_id):
        """동아리 공지 수정"""
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
            parser.add_argument("title", type=str, location="json")
            parser.add_argument("content", type=str, location="json")
            parser.add_argument("is_important", type=bool, location="json")
            args = parser.parse_args()

            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                return {
                    "status": "error",
                    "message": "수정할 데이터가 없습니다",
                    "code": "400-03",
                }, 400

            notice = update_notice(notice_id, update_data, club_id)
            return notice, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    @require_permission("notices.club_delete", club_id_param="club_id")
    def delete(self, club_id, notice_id):
        """동아리 공지 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            result = delete_notice(notice_id, club_id)
            return {"message": result["message"]}, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-05"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

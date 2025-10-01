from flask_restx import Resource, reqparse
from services.session_service import get_current_session
from services.home_service import (
    get_all_clubs,
    get_club_by_id,
    update_club_info,
    update_club_status,
    add_club_question,
    update_question,
    delete_question,
    get_club_members,
)


class ClubListController(Resource):
    """동아리 목록 조회 컨트롤러"""

    def get(self):
        """모든 동아리 목록을 반환합니다"""
        try:
            clubs_data = get_all_clubs()
            return {
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubUpdateController(Resource):
    """동아리 정보 조회/수정 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 상세 정보를 반환합니다"""
        try:
            club_data = get_club_by_id(club_id)
            if not club_data:
                return {
                    "status": "error",
                    "message": "해당 동아리를 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return club_data, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

    def patch(self, club_id):
        """동아리 정보를 수정합니다"""
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
            parser.add_argument("name", type=str, location="json")
            parser.add_argument("activity_summary", type=str, location="json")
            parser.add_argument("president_name", type=str, location="json")
            parser.add_argument("contact", type=str, location="json")
            parser.add_argument("category_id", type=int, location="json")
            args = parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                return {
                    "status": "error",
                    "message": "수정할 데이터가 없습니다",
                    "code": "400-03",
                }, 400

            club_data = update_club_info(club_id, update_data)
            return club_data, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubStatusController(Resource):
    """동아리 모집 상태 변경 컨트롤러"""

    def patch(self, club_id):
        """동아리 모집 상태를 변경합니다"""
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
            status = args["status"]

            update_club_status(club_id, status)
            return {
                "message": "동아리 모집 상태가 성공적으로 변경되었습니다.",
                "club_id": club_id,
                "recruitment_status": status,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-05"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubQuestionsController(Resource):
    """동아리 지원서 문항 추가 컨트롤러"""

    def post(self, club_id):
        """동아리 지원서 문항을 추가합니다"""
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
            parser.add_argument(
                "question_text", type=str, required=True, location="json"
            )
            args = parser.parse_args()
            question_data = {"question_text": args["question_text"]}

            new_question = add_club_question(club_id, question_data)
            return new_question, 201

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-07"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class QuestionController(Resource):
    """지원서 문항 수정/삭제 컨트롤러"""

    def patch(self, question_id):
        """지원서 문항을 수정합니다"""
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
            parser.add_argument("question_text", type=str, location="json")
            args = parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                return {
                    "status": "error",
                    "message": "수정할 데이터가 없습니다",
                    "code": "400-08",
                }, 400

            question_data = update_question(question_id, update_data)
            return question_data, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-09"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

    def delete(self, question_id):
        """지원서 문항을 삭제합니다"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            result = delete_question(question_id)
            return {"message": result["message"]}, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-10"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubMembersController(Resource):
    """동아리원 목록 조회 컨트롤러"""

    def get(self, club_id):
        """동아리원 목록을 조회합니다"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            members = get_club_members(club_id)
            return {
                "count": len(members),
                "members": members,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-11"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

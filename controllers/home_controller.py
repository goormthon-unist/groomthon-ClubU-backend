from flask_restx import Resource, abort, reqparse
from services.home_service import (
    get_all_clubs,
    get_club_by_id,
    get_open_clubs,
    update_club_info,
    update_club_status,
    get_club_questions,
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
                "status": "success",
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200
        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubUpdateController(Resource):
    """동아리 정보 수정 컨트롤러"""

    def patch(self, club_id):
        """동아리 정보를 수정합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, location="json")
            parser.add_argument("activity_summary", type=str, location="json")
            parser.add_argument("president_name", type=str, location="json")
            parser.add_argument("contact", type=str, location="json")
            parser.add_argument("category_id", type=int, location="json")
            args = parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                abort(400, "400-03: 수정할 데이터가 없습니다")

            club_data = update_club_info(club_id, update_data)
            return {"status": "success", "club": club_data}, 200

        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubStatusController(Resource):
    """동아리 모집 상태 변경 컨트롤러"""

    def patch(self, club_id):
        """동아리 모집 상태를 변경합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("status", type=str, required=True, location="json")
            args = parser.parse_args()
            status = args["status"]

            club_data = update_club_status(club_id, status)
            return {"status": "success", "club": club_data}, 200

        except ValueError as e:
            abort(400, f"400-05: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubQuestionsController(Resource):
    """동아리 지원서 문항 관리 컨트롤러"""

    def get(self, club_id):
        """동아리 지원서 문항을 조회합니다"""
        try:
            questions = get_club_questions(club_id)
            return {
                "status": "success",
                "count": len(questions),
                "questions": questions,
            }, 200

        except ValueError as e:
            abort(400, f"400-06: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def post(self, club_id):
        """동아리 지원서 문항을 추가합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "question_text", type=str, required=True, location="json"
            )

            args = parser.parse_args()
            question_data = {
                "question_text": args["question_text"],
            }

            new_question = add_club_question(club_id, question_data)
            return {"status": "success", "question": new_question}, 201

        except ValueError as e:
            abort(400, f"400-07: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class QuestionController(Resource):
    """지원서 문항 수정/삭제 컨트롤러"""

    def patch(self, question_id):
        """지원서 문항을 수정합니다"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("question_text", type=str, location="json")
            parser.add_argument("question_order", type=int, location="json")
            args = parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}

            if not update_data:
                abort(400, "400-08: 수정할 데이터가 없습니다")

            question_data = update_question(question_id, update_data)
            return {"status": "success", "question": question_data}, 200

        except ValueError as e:
            abort(400, f"400-09: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def delete(self, question_id):
        """지원서 문항을 삭제합니다"""
        try:
            result = delete_question(question_id)
            return {"status": "success", "message": result["message"]}, 200

        except ValueError as e:
            abort(400, f"400-10: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubMembersController(Resource):
    """동아리원 목록 조회 컨트롤러"""

    def get(self, club_id):
        """동아리원 목록을 조회합니다"""
        try:
            members = get_club_members(club_id)
            return {"status": "success", "count": len(members), "members": members}, 200

        except ValueError as e:
            abort(400, f"400-11: {str(e)}")
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

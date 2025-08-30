from flask_restx import Resource, abort
from flask import request
from services.application_check_submit_service import (
    get_club_application_questions,
    submit_application,
)


class ClubApplicationQuestionsController(Resource):
    """동아리 지원 질문 조회 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 지원 질문들을 반환합니다"""
        try:
            questions_data = get_club_application_questions(club_id)
            return {
                "status": "success",
                "club_id": club_id,
                "count": len(questions_data),
                "questions": questions_data,
            }, 200
        except ValueError as e:
            # 동아리가 없거나 질문이 없는 경우
            return {
                "status": "success",
                "club_id": club_id,
                "count": 0,
                "questions": [],
                "message": str(e),
            }, 200
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ApplicationSubmitController(Resource):
    """지원서 제출 컨트롤러"""

    def post(self, club_id):
        """동아리 지원서를 제출합니다"""
        try:
            # 요청 데이터 파싱
            data = request.get_json()
            if not data:
                abort(400, "400-01: 요청 데이터가 없습니다")

            user_id = data.get("user_id")
            answers = data.get("answers", [])

            # 필수 필드 검증
            if not user_id:
                abort(400, "400-02: user_id가 필요합니다")
            if not answers:
                abort(400, "400-03: 답변 데이터가 필요합니다")

            # 답변 데이터 검증
            for i, answer in enumerate(answers):
                if "question_id" not in answer:
                    abort(400, f"400-04: 답변 {i+1}에 question_id가 필요합니다")
                if "answer_text" not in answer:
                    abort(400, f"400-05: 답변 {i+1}에 answer_text가 필요합니다")

            # 지원서 제출
            result = submit_application(club_id, user_id, answers)

            return {
                "status": "success",
                "message": "지원서가 성공적으로 제출되었습니다",
                "data": result,
            }, 201

        except ValueError as e:
            abort(400, f"400-06: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

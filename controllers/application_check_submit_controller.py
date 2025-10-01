from flask_restx import Resource
from flask import request
from services.session_service import get_current_session
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
                "club_id": club_id,
                "count": len(questions_data),
                "questions": questions_data,
            }, 200
        except ValueError as e:
            # 동아리가 없거나 질문이 없는 경우
            return {
                "club_id": club_id,
                "count": 0,
                "questions": [],
                "message": str(e),
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ApplicationSubmitController(Resource):
    """지원서 제출 컨트롤러"""

    def post(self, club_id):
        """동아리 지원서를 제출합니다"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 요청 데이터 파싱
            data = request.get_json()
            if not data:
                return {
                    "status": "error",
                    "message": "요청 데이터가 없습니다",
                    "code": "400-01",
                }, 400

            # 세션에서 user_id 가져오기 (요청 데이터의 user_id 무시)
            user_id = session_data["user_id"]
            answers = data.get("answers", [])

            # 필수 필드 검증
            if not answers:
                return {
                    "status": "error",
                    "message": "답변 데이터가 필요합니다",
                    "code": "400-03",
                }, 400

            # 답변 데이터 검증
            for i, answer in enumerate(answers):
                if "question_id" not in answer:
                    return {
                        "status": "error",
                        "message": f"답변 {i+1}에 question_id가 필요합니다",
                        "code": "400-04",
                    }, 400
                if "answer_text" not in answer:
                    return {
                        "status": "error",
                        "message": f"답변 {i+1}에 answer_text가 필요합니다",
                        "code": "400-05",
                    }, 400

            # 지원서 제출
            result = submit_application(club_id, user_id, answers)

            return {
                "message": "지원서가 성공적으로 제출되었습니다",
                "application": result,
            }, 201

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-06"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

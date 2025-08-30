from flask_restx import Namespace, Resource
from controllers.application_check_submit_controller import (
    ClubApplicationQuestionsController,
    ApplicationSubmitController,
)

# 네임스페이스 등록
application_ns = Namespace("applications", description="지원서 관리 API")


# 디버깅용 임시 API
@application_ns.route("/debug/<int:club_id>")
class DebugResource(Resource):
    """디버깅용 임시 API"""

    def get(self, club_id):
        from models import Club, ClubApplicationQuestion

        try:
            # Step 1: 동아리 존재 확인
            club = Club.query.get(club_id)
            if not club:
                return {"step": 1, "error": "동아리가 존재하지 않음", "club_id": club_id}, 404

            # Step 2: 질문 조회
            questions = ClubApplicationQuestion.query.filter_by(club_id=club_id).all()

            return {
                "step": 2,
                "club_found": True,
                "club_name": club.name,
                "questions_count": len(questions),
                "questions": [{"id": q.id, "text": q.question_text} for q in questions],
            }, 200

        except Exception as e:
            return {"error": str(e), "type": type(e).__name__}, 500


# API 엔드포인트 등록
@application_ns.route("/clubs/<int:club_id>/application/questions")
class ClubApplicationQuestionsResource(ClubApplicationQuestionsController):
    """동아리 지원 질문 조회 리소스"""

    pass


@application_ns.route("/applications/<int:club_id>")
class ApplicationSubmitResource(ApplicationSubmitController):
    """지원서 제출 리소스"""

    pass

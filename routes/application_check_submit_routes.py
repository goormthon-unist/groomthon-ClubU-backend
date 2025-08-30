from flask_restx import Namespace, Resource
from controllers.application_check_submit_controller import (
    ClubApplicationQuestionsController,
    ApplicationSubmitController,
)
from models import Application, User, Club

# 네임스페이스 등록
application_ns = Namespace("applications", description="지원서 관리 API")


# API 엔드포인트 등록
@application_ns.route("/clubs/<int:club_id>/application/questions")
class ClubApplicationQuestionsResource(ClubApplicationQuestionsController):
    """동아리 지원 질문 조회 리소스"""

    pass


@application_ns.route("/applications/<int:club_id>")
class ApplicationSubmitResource(ApplicationSubmitController):
    """지원서 제출 리소스"""

    pass


@application_ns.route("/debug/<int:club_id>")
class DebugApplicationResource(Resource):
    """디버깅용 임시 API"""

    def post(self, club_id):
        from models import db
        from datetime import datetime

        try:
            # 1. 기본 검증
            club = Club.query.get(club_id)
            if not club:
                return {"step": 1, "error": "동아리가 존재하지 않음", "club_id": club_id}, 404

            # 2. 사용자 확인 (9001 고정)
            user = User.query.get(9001)
            if not user:
                return {"step": 2, "error": "사용자 9001이 존재하지 않음"}, 400

            # 3. Application 생성 테스트
            test_app = Application(
                user_id=9001,
                club_id=club_id,
                status="SUBMITTED",
                submitted_at=datetime.utcnow(),
            )
            db.session.add(test_app)
            db.session.flush()  # ID 확보 시도

            return {
                "step": 3,
                "success": True,
                "application_id": test_app.id,
                "user_found": True,
                "club_found": True,
                "club_name": club.name,
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "type": type(e).__name__, "step": "exception"}, 500

# services/application_check_submit_service.py

from datetime import datetime
from models import (
    db,
    ClubApplicationQuestion,
    Application,
    ApplicationAnswer,
    User,
    Club,
)


def get_club_application_questions(club_id: int):
    """특정 동아리의 지원 질문들을 조회 (order 보장)"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        # 질문 조회 (질문 순서 asc)
        questions = (
            ClubApplicationQuestion.query.filter_by(club_id=club_id)
            .order_by(ClubApplicationQuestion.question_order.asc())
            .all()
        )

        if not questions:
            raise ValueError("해당 동아리의 지원 질문이 없습니다")

        return [
            {
                "id": q.id,
                "question_text": q.question_text,
                "question_order": q.question_order,
            }
            for q in questions
        ]

    except ValueError:
        raise
    except Exception as e:
        # 상위 컨트롤러에서 500으로 처리
        raise Exception(f"지원 질문 조회 중 오류 발생: {str(e)}")


def submit_application(club_id: int, user_id: int, answers_data: list[dict]):
    """
    동아리 지원서 제출
    - DB 스키마 준수:
      * applications.status: ENUM('SUBMITTED','VIEWED','ACCEPTED','REJECTED')
      * applications.submitted_at: TIMESTAMP NOT NULL → 반드시 값 세팅
      * application_answers.answer_order: 해당 질문의 question_order와 동일
    """
    try:
        # --------- 0) 기본 엔터티 검증 ----------
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("존재하지 않는 사용자입니다")

        # 중복 지원 방지
        existing_application = Application.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()
        if existing_application:
            raise ValueError("이미 해당 동아리에 지원하셨습니다")

        # --------- 1) 질문 맵 구성 (id -> question_order) ----------
        rows = (
            ClubApplicationQuestion.query.filter_by(club_id=club_id)
            .with_entities(
                ClubApplicationQuestion.id, ClubApplicationQuestion.question_order
            )
            .all()
        )
        if not rows:
            raise ValueError("해당 동아리의 지원 질문이 없습니다")

        q_order_map = {int(qid): int(qorder) for (qid, qorder) in rows}

        # --------- 2) 요청 검증 ----------
        seen = set()
        for i, a in enumerate(answers_data, start=1):
            # 키 존재/타입 최소 검증
            if "question_id" not in a:
                raise ValueError(f"답변 {i}에 question_id가 필요합니다")
            if "answer_text" not in a:
                raise ValueError(f"답변 {i}에 answer_text가 필요합니다")

            try:
                qid = int(a["question_id"])
            except (TypeError, ValueError):
                raise ValueError(f"답변 {i}의 question_id 형식이 올바르지 않습니다")

            if qid not in q_order_map:
                raise ValueError(f"존재하지 않는 질문입니다: {qid}")

            if qid in seen:
                raise ValueError(f"질문 {qid}에 대한 중복 답변이 있습니다")
            seen.add(qid)

        # (선택) 모든 질문에 대해 답변을 강제하려면:
        # if len(seen) != len(q_order_map):
        #     raise ValueError("모든 질문에 대한 답변을 제출해야 합니다")

        # --------- 3) Application 생성 (submitted_at 필수) ----------
        new_application = Application(
            user_id=user_id,
            club_id=club_id,
            status="SUBMITTED",
            submitted_at=datetime.utcnow(),  # ✅ TIMESTAMP NOT NULL 충족
        )
        db.session.add(new_application)
        db.session.flush()  # PK 확보

        # --------- 4) Answer 저장 (order = question_order) ----------
        for a in answers_data:
            qid = int(a["question_id"])
            answer = ApplicationAnswer(
                application_id=new_application.id,
                question_id=qid,
                answer_text=a["answer_text"],
                answer_order=q_order_map[qid],  # ✅ 스키마 규칙
            )
            db.session.add(answer)

        # --------- 5) 커밋 ----------
        db.session.commit()

        return {
            "application_id": new_application.id,
            "status": new_application.status,
            "submitted_at": new_application.submitted_at.isoformat(),
        }

    except ValueError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 제출 중 오류 발생: {str(e)}")

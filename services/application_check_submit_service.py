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
    """특정 동아리의 지원 질문들을 조회 (DB 스키마 컬럼만 반환)"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        # ❗ 스키마에 있는 컬럼만 명시적으로 select (id, question_text, question_order)
        rows = (
            db.session.query(
                ClubApplicationQuestion.id,
                ClubApplicationQuestion.question_text,
                ClubApplicationQuestion.question_order,
            )
            .filter(ClubApplicationQuestion.club_id == club_id)
            .order_by(ClubApplicationQuestion.question_order.asc())
            .all()
        )

        if not rows:
            raise ValueError("해당 동아리의 지원 질문이 없습니다")

        # 튜플 -> dict
        return [
            {
                "id": r[0],
                "question_text": r[1],
                "question_order": r[2],
            }
            for r in rows
        ]

    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"지원 질문 조회 중 오류 발생: {str(e)}")


def submit_application(club_id: int, user_id: int, answers_data: list[dict]):
    """
    동아리 지원서 제출
    - applications.status: ENUM('SUBMITTED','VIEWED','ACCEPTED','REJECTED')
    - applications.submitted_at: TIMESTAMP NOT NULL → 반드시 값 세팅
    - application_answers.answer_order = 해당 질문의 question_order
    """
    try:
        # 0) 엔터티 검증
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("존재하지 않는 사용자입니다")

        existing = Application.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()
        if existing:
            raise ValueError("이미 해당 동아리에 지원하셨습니다")

        # 1) 질문 맵(id -> order) — 스키마 컬럼만 select
        q_rows = (
            db.session.query(
                ClubApplicationQuestion.id,
                ClubApplicationQuestion.question_order,
            )
            .filter(ClubApplicationQuestion.club_id == club_id)
            .all()
        )
        if not q_rows:
            raise ValueError("해당 동아리의 지원 질문이 없습니다")

        q_order_map = {int(qid): int(qorder) for (qid, qorder) in q_rows}

        # 2) 요청 검증
        seen = set()
        for i, a in enumerate(answers_data, start=1):
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

        # 3) Application 생성 (submitted_at 필수)
        new_app = Application(
            user_id=user_id,
            club_id=club_id,
            status="SUBMITTED",
            submitted_at=datetime.utcnow(),  # TIMESTAMP NOT NULL
        )
        db.session.add(new_app)
        db.session.flush()  # id 확보

        # 4) Answer 저장 (order = question_order)
        for a in answers_data:
            qid = int(a["question_id"])
            db.session.add(
                ApplicationAnswer(
                    application_id=new_app.id,
                    question_id=qid,
                    answer_text=a["answer_text"],
                    answer_order=q_order_map[qid],
                )
            )

        # 5) 커밋
        db.session.commit()

        return {
            "application_id": new_app.id,
            "status": new_app.status,
            "submitted_at": new_app.submitted_at.isoformat(),
        }

    except ValueError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 제출 중 오류 발생: {str(e)}")

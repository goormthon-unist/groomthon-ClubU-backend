from models import (
    db,
    ClubApplicationQuestion,
    Application,
    ApplicationAnswer,
    User,
    Club,
)


def get_club_application_questions(club_id):
    """특정 동아리의 지원 질문들을 조회"""
    try:
        # 동아리 존재 여부 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        # 해당 동아리의 지원 질문들 조회 (간단한 방식)
        questions = ClubApplicationQuestion.query.filter_by(club_id=club_id).all()

        if not questions:
            raise ValueError("해당 동아리의 지원 질문이 없습니다")

        # 수동으로 정렬 (Python에서)
        questions_sorted = sorted(questions, key=lambda q: q.question_order)

        # JSON 변환
        return [
            {
                "id": question.id,
                "question_text": question.question_text,
                "question_order": question.question_order,
            }
            for question in questions_sorted
        ]

    except ValueError:
        # ValueError는 그대로 전달
        raise
    except Exception as e:
        # 다른 데이터베이스 오류를 상위로 전달
        raise Exception(f"지원 질문 조회 중 오류 발생: {str(e)}")


def submit_application(club_id, user_id, answers_data):
    """동아리 지원서 제출"""
    try:
        # 동아리 존재 여부 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("존재하지 않는 동아리입니다")

        # 사용자 존재 여부 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError("존재하지 않는 사용자입니다")

        # 이미 지원했는지 확인
        existing_application = Application.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()
        if existing_application:
            raise ValueError("이미 해당 동아리에 지원하셨습니다")

        # 지원서 생성
        new_application = Application(
            user_id=user_id,
            club_id=club_id,
            status="SUBMITTED",  # 기본 상태: 제출됨
        )
        db.session.add(new_application)
        db.session.flush()  # ID를 얻기 위해 flush

        # 답변들 저장
        for answer_data in answers_data:
            # 질문 존재 여부 확인
            question = ClubApplicationQuestion.query.filter_by(
                id=answer_data["question_id"], club_id=club_id
            ).first()
            if not question:
                raise ValueError(f"존재하지 않는 질문입니다: {answer_data['question_id']}")

            # 답변 저장
            new_answer = ApplicationAnswer(
                application_id=new_application.id,
                question_id=answer_data["question_id"],
                answer_text=answer_data["answer_text"],
                answer_order=answer_data.get("answer_order", 1),
            )
            db.session.add(new_answer)

        # 모든 변경사항 커밋
        db.session.commit()

        return {
            "application_id": new_application.id,
            "status": new_application.status,
            "submitted_at": new_application.submitted_at.isoformat()
            if new_application.submitted_at
            else None,
        }

    except ValueError:
        # ValueError는 그대로 전달
        db.session.rollback()
        raise
    except Exception as e:
        # 다른 오류 발생 시 롤백
        db.session.rollback()
        raise Exception(f"지원서 제출 중 오류 발생: {str(e)}")

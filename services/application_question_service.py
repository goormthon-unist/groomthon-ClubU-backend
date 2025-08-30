from models import db, ClubApplicationQuestion, Club


def get_club_questions(club_id):
    """동아리 지원서 문항 조회"""
    try:
        questions = (
            db.session.query(ClubApplicationQuestion)
            .filter(ClubApplicationQuestion.club_id == club_id)
            .order_by(ClubApplicationQuestion.question_order)
            .all()
        )

        return [
            {
                "id": question.id,
                "club_id": question.club_id,
                "question_text": question.question_text,
                "question_order": question.question_order,
            }
            for question in questions
        ]

    except Exception as e:
        raise Exception(f"지원서 문항 조회 중 오류 발생: {str(e)}")


def create_club_question(club_id, question_data):
    """동아리 지원서 문항 추가"""
    try:
        # 동아리 존재 확인
        club = db.session.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 새로운 문항 생성
        new_question = ClubApplicationQuestion(
            club_id=club_id,
            question_text=question_data["question_text"],
            question_order=question_data.get("question_order", 0)
        )

        db.session.add(new_question)
        db.session.commit()

        return {
            "id": new_question.id,
            "club_id": new_question.club_id,
            "question_text": new_question.question_text,
            "question_order": new_question.question_order,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 문항 추가 중 오류 발생: {str(e)}")


def update_club_question(question_id, update_data):
    """동아리 지원서 문항 수정"""
    try:
        question = (
            db.session.query(ClubApplicationQuestion)
            .filter(ClubApplicationQuestion.id == question_id)
            .first()
        )

        if not question:
            raise ValueError("해당 문항을 찾을 수 없습니다")

        # 수정 가능한 필드들
        allowed_fields = ["question_text", "question_order"]
        
        for field in allowed_fields:
            if field in update_data:
                setattr(question, field, update_data[field])

        db.session.commit()

        return {
            "id": question.id,
            "club_id": question.club_id,
            "question_text": question.question_text,
            "question_order": question.question_order,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 문항 수정 중 오류 발생: {str(e)}")


def delete_club_question(question_id):
    """동아리 지원서 문항 삭제"""
    try:
        question = (
            db.session.query(ClubApplicationQuestion)
            .filter(ClubApplicationQuestion.id == question_id)
            .first()
        )

        if not question:
            raise ValueError("해당 문항을 찾을 수 없습니다")

        db.session.delete(question)
        db.session.commit()

        return {"message": "문항이 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 문항 삭제 중 오류 발생: {str(e)}")

from models import db, Club, ClubCategory, ClubApplicationQuestion, ClubMember


def get_all_clubs():
    """모든 동아리 정보를 카테고리와 함께 조회"""
    try:
        # 동아리와 카테고리 정보를 함께 조회
        clubs = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .all()
        )

        if not clubs:
            raise ValueError("등록된 동아리가 없습니다")

        # JSON 변환
        return [
            {
                "id": club.id,
                "name": club.name,
                "activity_summary": club.activity_summary,
                "category": {"id": category.id, "name": category.name},
                "recruitment_status": club.recruitment_status,
                "created_at": (
                    club.created_at.isoformat() if club.created_at else None
                ),
                "updated_at": (
                    club.updated_at.isoformat() if club.updated_at else None
                ),
            }
            for club, category in clubs
        ]

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"동아리 목록 조회 중 오류 발생: {str(e)}")


def get_club_by_id(club_id):
    """특정 동아리의 상세 정보를 조회"""
    try:
        club_data = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Club.id == club_id)
            .first()
        )

        if not club_data:
            return None

        club, category = club_data

        # JSON 변환
        return {
            "id": club.id,
            "name": club.name,
            "activity_summary": club.activity_summary,
            "category": {"id": category.id, "name": category.name},
            "recruitment_status": club.recruitment_status,
            "president_name": club.president_name,
            "contact": club.contact,
            "created_at": club.created_at.isoformat() if club.created_at else None,
            "updated_at": club.updated_at.isoformat() if club.updated_at else None,
        }

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"동아리 상세 조회 중 오류 발생: {str(e)}")


def update_club_info(club_id, update_data):
    """동아리 정보 수정"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 업데이트 가능한 필드들
        allowed_fields = [
            "name", "activity_summary", "president_name", 
            "contact", "category_id"
        ]
        
        for field in allowed_fields:
            if field in update_data:
                setattr(club, field, update_data[field])

        db.session.commit()
        return get_club_by_id(club_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 정보 수정 중 오류 발생: {str(e)}")


def update_club_status(club_id, status):
    """동아리 모집 상태 변경"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        if status not in ["recruiting", "closed"]:
            raise ValueError("유효하지 않은 모집 상태입니다")

        club.recruitment_status = status
        db.session.commit()
        
        return get_club_by_id(club_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 상태 변경 중 오류 발생: {str(e)}")


def get_club_questions(club_id):
    """동아리 지원서 문항 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        questions = ClubApplicationQuestion.query.filter_by(club_id=club_id).all()
        
        return [
            {
                "id": question.id,
                "club_id": question.club_id,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "is_required": question.is_required,
                "order": question.order,
                "created_at": question.created_at.isoformat() if question.created_at else None,
            }
            for question in questions
        ]

    except Exception as e:
        raise Exception(f"지원서 문항 조회 중 오류 발생: {str(e)}")


def add_club_question(club_id, question_data):
    """동아리 지원서 문항 추가"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 기존 문항들의 최대 order 값 찾기
        max_order = db.session.query(db.func.max(ClubApplicationQuestion.order))\
            .filter_by(club_id=club_id).scalar() or 0

        new_question = ClubApplicationQuestion(
            club_id=club_id,
            question_text=question_data["question_text"],
            question_type=question_data.get("question_type", "text"),
            is_required=question_data.get("is_required", True),
            order=max_order + 1
        )

        db.session.add(new_question)
        db.session.commit()

        return {
            "id": new_question.id,
            "club_id": new_question.club_id,
            "question_text": new_question.question_text,
            "question_type": new_question.question_type,
            "is_required": new_question.is_required,
            "order": new_question.order,
            "created_at": new_question.created_at.isoformat() if new_question.created_at else None,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 문항 추가 중 오류 발생: {str(e)}")


def update_question(question_id, update_data):
    """지원서 문항 수정"""
    try:
        question = ClubApplicationQuestion.query.get(question_id)
        if not question:
            raise ValueError("해당 문항을 찾을 수 없습니다")

        # 업데이트 가능한 필드들
        allowed_fields = ["question_text", "question_type", "is_required"]
        
        for field in allowed_fields:
            if field in update_data:
                setattr(question, field, update_data[field])

        db.session.commit()

        return {
            "id": question.id,
            "club_id": question.club_id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "is_required": question.is_required,
            "order": question.order,
            "created_at": question.created_at.isoformat() if question.created_at else None,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"문항 수정 중 오류 발생: {str(e)}")


def delete_question(question_id):
    """지원서 문항 삭제"""
    try:
        question = ClubApplicationQuestion.query.get(question_id)
        if not question:
            raise ValueError("해당 문항을 찾을 수 없습니다")

        db.session.delete(question)
        db.session.commit()

        return {"message": "문항이 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"문항 삭제 중 오류 발생: {str(e)}")


def get_club_members(club_id):
    """동아리원 목록 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        members = ClubMember.query.filter_by(club_id=club_id).all()
        
        return [
            {
                "id": member.id,
                "club_id": member.club_id,
                "user_id": member.user_id,
                "role": member.role,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
            }
            for member in members
        ]

    except Exception as e:
        raise Exception(f"동아리원 목록 조회 중 오류 발생: {str(e)}")

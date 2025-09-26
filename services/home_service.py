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
                "president_name": club.president_name,
                "contact": club.contact,
                "current_generation": club.current_generation,
                "introduction": club.introduction,
                "recruitment_start": (
                    club.recruitment_start.isoformat()
                    if club.recruitment_start
                    else None
                ),
                "recruitment_finish": (
                    club.recruitment_finish.isoformat()
                    if club.recruitment_finish
                    else None
                ),
                "logo_image": club.logo_image,
                "introduction_image": club.introduction_image,
                "club_room": club.club_room,
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
            "current_generation": club.current_generation,
            "introduction": club.introduction,
            "recruitment_start": (
                club.recruitment_start.isoformat() if club.recruitment_start else None
            ),
            "recruitment_finish": (
                club.recruitment_finish.isoformat() if club.recruitment_finish else None
            ),
            "logo_image": club.logo_image,
            "introduction_image": club.introduction_image,
            "club_room": club.club_room,
            "created_at": (club.created_at.isoformat() if club.created_at else None),
            "updated_at": (club.updated_at.isoformat() if club.updated_at else None),
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
            "name",
            "activity_summary",
            "president_name",
            "contact",
            "category_id",
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

        if status not in ["OPEN", "CLOSED"]:
            raise ValueError("유효하지 않은 모집 상태입니다")

        club.recruitment_status = status
        db.session.commit()

        return True

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
                "order": question.question_order,
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
        max_order = (
            db.session.query(db.func.max(ClubApplicationQuestion.question_order))
            .filter_by(club_id=club_id)
            .scalar()
            or 0
        )

        new_question = ClubApplicationQuestion(
            club_id=club_id,
            question_text=question_data["question_text"],
            question_order=max_order + 1,
        )

        db.session.add(new_question)
        db.session.commit()

        return {
            "id": new_question.id,
            "club_id": new_question.club_id,
            "question_text": new_question.question_text,
            "order": new_question.question_order,
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
        allowed_fields = ["question_text"]

        for field in allowed_fields:
            if field in update_data:
                setattr(question, field, update_data[field])

        db.session.commit()

        return {
            "id": question.id,
            "club_id": question.club_id,
            "question_text": question.question_text,
            "order": question.question_order,
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


def get_open_clubs():
    """모집 중인 동아리 정보를 카테고리와 함께 조회"""
    try:
        # 모집 중인 동아리와 카테고리 정보를 함께 조회
        clubs = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Club.recruitment_status == "OPEN")
            .all()
        )

        if not clubs:
            return []  # 빈 리스트 반환 (에러가 아님)

        # JSON 변환 - 요청된 형식에 맞춰 모든 필드 포함
        return [
            {
                "id": club.id,
                "name": club.name,
                "category": {"id": category.id, "name": category.name},
                "activity_summary": club.activity_summary,
                "introduction": club.introduction,
                "recruitment_status": club.recruitment_status,
                "current_generation": club.current_generation,
                "president_name": club.president_name,
                "contact": club.contact,
                "recruitment_start": (
                    club.recruitment_start.isoformat()
                    if club.recruitment_start
                    else None
                ),
                "recruitment_finish": (
                    club.recruitment_finish.isoformat()
                    if club.recruitment_finish
                    else None
                ),
                "logo_image": club.logo_image,
                "introduction_image": club.introduction_image,
                "club_room": club.club_room,
                "created_at": (
                    club.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                    if club.created_at
                    else None
                ),
                "updated_at": (
                    club.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                    if club.updated_at
                    else None
                ),
            }
            for club, category in clubs
        ]

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"모집 중인 동아리 목록 조회 중 오류 발생: {str(e)}")


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
                "role_id": member.role_id,
                "generation": member.generation,
                "other_info": member.other_info,
                "joined_at": (
                    member.joined_at.isoformat() if member.joined_at else None
                ),
            }
            for member in members
        ]

    except Exception as e:
        raise Exception(f"동아리원 목록 조회 중 오류 발생: {str(e)}")

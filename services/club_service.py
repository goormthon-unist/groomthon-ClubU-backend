from models import db, Club, ClubCategory, ClubMember, User, Role


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
                "created_at": club.created_at.isoformat() if club.created_at else None,
                "updated_at": club.updated_at.isoformat() if club.updated_at else None,
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
        club = db.session.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 수정 가능한 필드들
        allowed_fields = [
            "name", "category_id", "activity_summary", "president_name", 
            "contact", "current_generation", "introduction"
        ]
        
        for field in allowed_fields:
            if field in update_data:
                setattr(club, field, update_data[field])

        db.session.commit()
        
        # 업데이트된 동아리 정보 반환
        return get_club_by_id(club_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 정보 수정 중 오류 발생: {str(e)}")


def update_club_status(club_id, status):
    """동아리 모집 상태 변경"""
    try:
        club = db.session.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        if status not in ["OPEN", "CLOSED"]:
            raise ValueError("유효하지 않은 모집 상태입니다")

        club.recruitment_status = status
        db.session.commit()
        
        return {
            "id": club.id,
            "name": club.name,
            "recruitment_status": club.recruitment_status,
            "updated_at": club.updated_at.isoformat() if club.updated_at else None,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 모집 상태 변경 중 오류 발생: {str(e)}")


def get_club_members(club_id):
    """동아리원 목록 조회"""
    try:
        members = (
            db.session.query(ClubMember, User, Role)
            .join(User, ClubMember.user_id == User.id)
            .outerjoin(Role, ClubMember.role_id == Role.id)
            .filter(ClubMember.club_id == club_id)
            .all()
        )

        if not members:
            return []

        # JSON 변환
        return [
            {
                "id": member.id,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "student_id": user.student_id,
                },
                "role": {
                    "id": role.id,
                    "name": role.name,
                } if role else None,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
            }
            for member, user, role in members
        ]

    except Exception as e:
        raise Exception(f"동아리원 목록 조회 중 오류 발생: {str(e)}")

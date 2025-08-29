from models import db, Club, ClubCategory


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

from models import db, Notice, Club


def create_notice(club_id, notice_data):
    """동아리 공지 생성"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 공지 생성
        new_notice = Notice(
            club_id=club_id,
            title=notice_data["title"],
            content=notice_data["content"],
            is_important=notice_data.get("is_important", False),
        )

        db.session.add(new_notice)
        db.session.commit()

        return {
            "id": new_notice.id,
            "club_id": new_notice.club_id,
            "title": new_notice.title,
            "content": new_notice.content,
            "is_important": new_notice.is_important,
            "created_at": new_notice.created_at.isoformat(),
            "updated_at": new_notice.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 생성 중 오류 발생: {str(e)}")


def get_club_notices(club_id):
    """특정 동아리의 공지 목록 조회"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        notices = (
            Notice.query.filter_by(club_id=club_id)
            .order_by(Notice.created_at.desc())
            .all()
        )

        return [
            {
                "id": notice.id,
                "club_id": notice.club_id,
                "title": notice.title,
                "content": notice.content,
                "is_important": notice.is_important,
                "created_at": notice.created_at.isoformat(),
                "updated_at": notice.updated_at.isoformat(),
            }
            for notice in notices
        ]

    except Exception as e:
        raise Exception(f"동아리 공지 조회 중 오류 발생: {str(e)}")


def get_all_notices():
    """전체 공지 목록 조회"""
    try:
        notices = (
            db.session.query(Notice, Club)
            .join(Club, Notice.club_id == Club.id)
            .order_by(Notice.created_at.desc())
            .all()
        )

        return [
            {
                "id": notice.id,
                "club_id": notice.club_id,
                "club_name": club.name,
                "title": notice.title,
                "content": notice.content,
                "is_important": notice.is_important,
                "created_at": notice.created_at.isoformat(),
                "updated_at": notice.updated_at.isoformat(),
            }
            for notice, club in notices
        ]

    except Exception as e:
        raise Exception(f"전체 공지 조회 중 오류 발생: {str(e)}")


def get_notice_by_id(notice_id):
    """공지 상세 조회"""
    try:
        notice_data = (
            db.session.query(Notice, Club)
            .join(Club, Notice.club_id == Club.id)
            .filter(Notice.id == notice_id)
            .first()
        )

        if not notice_data:
            return None

        notice, club = notice_data

        return {
            "id": notice.id,
            "club_id": notice.club_id,
            "club_name": club.name,
            "title": notice.title,
            "content": notice.content,
            "is_important": notice.is_important,
            "created_at": notice.created_at.isoformat(),
            "updated_at": notice.updated_at.isoformat(),
        }

    except Exception as e:
        raise Exception(f"공지 상세 조회 중 오류 발생: {str(e)}")


def update_notice(notice_id, update_data):
    """공지 수정"""
    try:
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("해당 공지를 찾을 수 없습니다")

        # 업데이트 가능한 필드들
        allowed_fields = ["title", "content", "is_important"]

        for field in allowed_fields:
            if field in update_data:
                setattr(notice, field, update_data[field])

        db.session.commit()

        return {
            "id": notice.id,
            "club_id": notice.club_id,
            "title": notice.title,
            "content": notice.content,
            "is_important": notice.is_important,
            "created_at": notice.created_at.isoformat(),
            "updated_at": notice.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 수정 중 오류 발생: {str(e)}")


def delete_notice(notice_id):
    """공지 삭제"""
    try:
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("해당 공지를 찾을 수 없습니다")

        db.session.delete(notice)
        db.session.commit()

        return {"message": "공지가 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 삭제 중 오류 발생: {str(e)}")

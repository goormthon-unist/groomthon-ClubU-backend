from models import Club, Notice, NoticeAsset, db


def create_notice(club_id, user_id, notice_data):
    """동아리 공지 생성"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 공지 생성
        new_notice = Notice(
            club_id=club_id,
            user_id=user_id,
            title=notice_data["title"],
            content=notice_data["content"],
            is_important=notice_data.get("is_important", False),
        )

        db.session.add(new_notice)
        db.session.commit()

        return {
            "id": new_notice.id,
            "club_id": new_notice.club_id,
            "user_id": new_notice.user_id,
            "title": new_notice.title,
            "content": new_notice.content,
            "status": new_notice.status,
            "is_important": new_notice.is_important,
            "views": new_notice.views,
            "posted_at": new_notice.posted_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 생성 중 오류 발생: {e}")


def get_club_notices(club_id):
    """특정 동아리의 공지 목록 조회 (첨부파일 포함)"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        notices = (
            Notice.query.filter_by(club_id=club_id, status="POSTED")
            .order_by(Notice.posted_at.desc())
            .all()
        )

        result = []
        for notice in notices:
            # 각 공지의 첨부파일 조회
            assets = NoticeAsset.query.filter_by(notices_id=notice.id).all()
            attachments = [
                {
                    "id": asset.id,
                    "asset_type": asset.asset_type,
                    "file_url": asset.file_url,
                    "created_at": asset.created_at.isoformat(),
                }
                for asset in assets
            ]

            result.append(
                {
                    "id": notice.id,
                    "club_id": notice.club_id,
                    "user_id": notice.user_id,
                    "title": notice.title,
                    "content": notice.content,
                    "status": notice.status,
                    "is_important": notice.is_important,
                    "views": notice.views,
                    "posted_at": notice.posted_at.isoformat(),
                    "attachments": attachments,
                }
            )

        return result

    except Exception as e:
        raise Exception(f"동아리 공지 조회 중 오류 발생: {e}")


def get_all_notices():
    """전체 공지 목록 조회 (첨부파일 포함)"""
    try:
        notices = (
            db.session.query(Notice, Club)
            .join(Club, Notice.club_id == Club.id)
            .filter(Notice.status == "POSTED")
            .order_by(Notice.posted_at.desc())
            .all()
        )

        result = []
        for notice, club in notices:
            # 각 공지의 첨부파일 조회
            assets = NoticeAsset.query.filter_by(notices_id=notice.id).all()
            attachments = [
                {
                    "id": asset.id,
                    "asset_type": asset.asset_type,
                    "file_url": asset.file_url,
                    "created_at": asset.created_at.isoformat(),
                }
                for asset in assets
            ]

            result.append(
                {
                    "id": notice.id,
                    "club_id": notice.club_id,
                    "user_id": notice.user_id,
                    "club_name": club.name,
                    "title": notice.title,
                    "content": notice.content,
                    "status": notice.status,
                    "is_important": notice.is_important,
                    "views": notice.views,
                    "posted_at": notice.posted_at.isoformat(),
                    "attachments": attachments,
                }
            )

        return result

    except Exception as e:
        raise Exception(f"전체 공지 조회 중 오류 발생: {e}")


def get_notice_by_id(notice_id):
    """공지 상세 조회 (첨부파일 포함)"""
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

        # 조회수 증가
        notice.views += 1
        db.session.commit()

        # 첨부파일 조회
        assets = NoticeAsset.query.filter_by(notices_id=notice_id).all()
        attachments = [
            {
                "id": asset.id,
                "asset_type": asset.asset_type,
                "file_url": asset.file_url,
                "created_at": asset.created_at.isoformat(),
            }
            for asset in assets
        ]

        return {
            "id": notice.id,
            "club_id": notice.club_id,
            "user_id": notice.user_id,
            "club_name": club.name,
            "title": notice.title,
            "content": notice.content,
            "status": notice.status,
            "is_important": notice.is_important,
            "views": notice.views,
            "posted_at": notice.posted_at.isoformat(),
            "attachments": attachments,
        }

    except Exception as e:
        raise Exception(f"공지 상세 조회 중 오류 발생: {e}")


def update_notice(notice_id, update_data, club_id=None):
    """공지 수정"""
    try:
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("해당 공지를 찾을 수 없습니다")

        # club_id가 제공된 경우 해당 동아리의 공지인지 확인
        if club_id is not None and notice.club_id != club_id:
            raise ValueError("해당 동아리의 공지가 아닙니다")

        # 업데이트 가능한 필드들
        allowed_fields = ["title", "content", "is_important"]

        for field in allowed_fields:
            if field in update_data:
                setattr(notice, field, update_data[field])

        db.session.commit()

        return {
            "id": notice.id,
            "club_id": notice.club_id,
            "user_id": notice.user_id,
            "title": notice.title,
            "content": notice.content,
            "status": notice.status,
            "is_important": notice.is_important,
            "views": notice.views,
            "posted_at": notice.posted_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 수정 중 오류 발생: {e}")


def delete_notice(notice_id, club_id=None):
    """공지 삭제 (상태를 DELETE로 변경)"""
    try:
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("해당 공지를 찾을 수 없습니다")

        # club_id가 제공된 경우 해당 동아리의 공지인지 확인
        if club_id is not None and notice.club_id != club_id:
            raise ValueError("해당 동아리의 공지가 아닙니다")

        notice.status = "DELETE"
        db.session.commit()

        return {"message": "공지가 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"공지 삭제 중 오류 발생: {e}")

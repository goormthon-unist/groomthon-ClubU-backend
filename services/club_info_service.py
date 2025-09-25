from models import Club, ClubMember, db
from utils.image_utils import save_club_image, delete_club_image


def update_club_introduction(club_id, introduction):
    """동아리 소개글 업데이트"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        club.introduction = introduction
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "introduction": club.introduction,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 소개글 업데이트 중 오류 발생: {e}")


def delete_club_introduction(club_id):
    """동아리 소개글 삭제"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        club.introduction = None
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "introduction": club.introduction,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 소개글 삭제 중 오류 발생: {e}")


def update_club_logo_image(club_id, image_file):
    """동아리 로고 이미지 업데이트"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 기존 이미지 삭제
        if club.logo_image:
            old_file_path = club.logo_image.replace("/clubs/", "clubs/")
            delete_club_image(old_file_path)

        # 새 이미지 저장
        image_info = save_club_image(image_file, club_id, "logo")
        club.logo_image = image_info["file_path"]
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "logo_image": club.logo_image,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 로고 이미지 업데이트 중 오류 발생: {e}")


def delete_club_logo_image(club_id):
    """동아리 로고 이미지 삭제"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 기존 이미지 삭제
        if club.logo_image:
            old_file_path = club.logo_image.replace("/clubs/", "clubs/")
            delete_club_image(old_file_path)

        club.logo_image = None
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "logo_image": club.logo_image,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 로고 이미지 삭제 중 오류 발생: {e}")


def update_club_introduction_image(club_id, image_file):
    """동아리 소개글 이미지 업데이트"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 기존 이미지 삭제
        if club.introduction_image:
            old_file_path = club.introduction_image.replace("/clubs/", "clubs/")
            delete_club_image(old_file_path)

        # 새 이미지 저장
        image_info = save_club_image(image_file, club_id, "introduction")
        club.introduction_image = image_info["file_path"]
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "introduction_image": club.introduction_image,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 소개글 이미지 업데이트 중 오류 발생: {e}")


def delete_club_introduction_image(club_id):
    """동아리 소개글 이미지 삭제"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 기존 이미지 삭제
        if club.introduction_image:
            old_file_path = club.introduction_image.replace("/clubs/", "clubs/")
            delete_club_image(old_file_path)

        club.introduction_image = None
        db.session.commit()

        return {
            "id": club.id,
            "name": club.name,
            "introduction_image": club.introduction_image,
            "updated_at": club.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 소개글 이미지 삭제 중 오류 발생: {e}")


def check_club_president_permission(user_id, club_id):
    """사용자가 해당 동아리의 회장인지 확인"""
    try:
        # 동아리 회장 권한 확인
        club_member = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id, role_id=4  # CLUB_PRESIDENT
        ).first()

        if not club_member:
            raise ValueError("동아리 회장 권한이 필요합니다")

        return True

    except Exception as e:
        raise Exception(f"권한 확인 중 오류 발생: {e}")

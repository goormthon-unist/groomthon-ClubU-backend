from datetime import datetime
from models import Banner, Club, db
from utils.image_utils import delete_banner_image, save_banner_image


def create_banner(club_id, user_id, banner_data, image_file):
    """배너 생성"""
    try:
        from flask import current_app

        current_app.logger.info(
            f"Creating banner for club_id: {club_id}, user_id: {user_id}"
        )

        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            current_app.logger.error(f"Club not found: {club_id}")
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 이미지 저장 및 최적화
        current_app.logger.info(f"Saving banner image for club_id: {club_id}")
        image_info = save_banner_image(image_file, club_id)

        # 날짜 변환
        start_date = datetime.strptime(banner_data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(banner_data["end_date"], "%Y-%m-%d").date()

        # 배너 생성
        new_banner = Banner(
            club_id=club_id,
            user_id=user_id,
            file_path=image_info["file_path"],
            position=banner_data.get("position", "TOP"),
            status="WAITING",
            start_date=start_date,
            end_date=end_date,
            title=banner_data["title"],
            description=banner_data.get("description", ""),
        )

        db.session.add(new_banner)
        db.session.commit()

        current_app.logger.info(f"Banner created successfully: {new_banner.id}")

        return {
            "id": new_banner.id,
            "club_id": new_banner.club_id,
            "user_id": new_banner.user_id,
            "file_path": new_banner.file_path,
            "position": new_banner.position,
            "status": new_banner.status,
            "uploaded_at": new_banner.uploaded_at.isoformat(),
            "start_date": new_banner.start_date.isoformat(),
            "end_date": new_banner.end_date.isoformat(),
            "title": new_banner.title,
            "description": new_banner.description,
        }

    except Exception as e:
        from flask import current_app

        db.session.rollback()
        current_app.logger.exception(f"Banner creation failed: {str(e)}")
        raise Exception(f"배너 생성 중 오류 발생: {e}")


def get_banners(status=None, position=None):
    """배너 목록 조회"""
    try:
        query = db.session.query(Banner, Club).join(Club, Banner.club_id == Club.id)

        if status:
            query = query.filter(Banner.status == status)
        if position:
            query = query.filter(Banner.position == position)

        banners = query.order_by(Banner.uploaded_at.desc()).all()

        return [
            {
                "id": banner.id,
                "club_id": banner.club_id,
                "user_id": banner.user_id,
                "club_name": club.name,
                "file_path": banner.file_path,
                "clublogoImageUrl": club.logo_image,
                "position": banner.position,
                "status": banner.status,
                "uploaded_at": banner.uploaded_at.isoformat(),
                "start_date": banner.start_date.isoformat(),
                "end_date": banner.end_date.isoformat(),
                "title": banner.title,
                "description": banner.description,
            }
            for banner, club in banners
        ]

    except Exception as e:
        raise Exception(f"배너 목록 조회 중 오류 발생: {e}")


def get_banner_by_id(banner_id):
    """배너 상세 조회"""
    try:
        banner_data = (
            db.session.query(Banner, Club)
            .join(Club, Banner.club_id == Club.id)
            .filter(Banner.id == banner_id)
            .first()
        )

        if not banner_data:
            return None

        banner, club = banner_data

        return {
            "id": banner.id,
            "club_id": banner.club_id,
            "user_id": banner.user_id,
            "club_name": club.name,
            "file_path": banner.file_path,
            "clublogoImageUrl": club.logo_image,
            "position": banner.position,
            "status": banner.status,
            "uploaded_at": banner.uploaded_at.isoformat(),
            "start_date": banner.start_date.isoformat(),
            "end_date": banner.end_date.isoformat(),
            "title": banner.title,
            "description": banner.description,
        }

    except Exception as e:
        raise Exception(f"배너 상세 조회 중 오류 발생: {e}")


def update_banner_status(banner_id, status):
    """배너 상태 변경"""
    try:
        banner = Banner.query.get(banner_id)
        if not banner:
            raise ValueError("해당 배너를 찾을 수 없습니다")

        valid_statuses = ["WAITING", "POSTED", "REJECTED", "ARCHIVED"]
        if status not in valid_statuses:
            raise ValueError("유효하지 않은 상태입니다")

        banner.status = status
        db.session.commit()

        return {
            "id": banner.id,
            "club_id": banner.club_id,
            "user_id": banner.user_id,
            "title": banner.title,
            "status": banner.status,
            "uploaded_at": banner.uploaded_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 상태 변경 중 오류 발생: {e}")


def delete_banner(banner_id):
    """배너 삭제"""
    try:
        banner = Banner.query.get(banner_id)
        if not banner:
            raise ValueError("해당 배너를 찾을 수 없습니다")

        # 이미지 파일 삭제
        file_path = banner.file_path.replace("/banners/", "banners/")
        delete_banner_image(file_path)

        db.session.delete(banner)
        db.session.commit()

        return {"message": "배너가 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 삭제 중 오류 발생: {e}")

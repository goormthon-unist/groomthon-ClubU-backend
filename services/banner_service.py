from datetime import datetime
from models import db, Banner, Club
from utils.image_utils import save_banner_image, delete_banner_images


def create_banner(club_id, banner_data, image_file):
    """배너 생성"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 이미지 저장 및 최적화
        image_info = save_banner_image(image_file, club_id)

        # 배너 생성
        new_banner = Banner(
            club_id=club_id,
            title=banner_data["title"],
            description=banner_data.get("description", ""),
            image_url=image_info["optimized_url"],
            original_image_url=image_info[
                "original_url"
            ],  # URL은 유지하되 실제 파일은 삭제됨
            location=banner_data.get("location", "MAIN_TOP"),
            status="PENDING",
            start_date=banner_data.get("start_date"),
            end_date=banner_data.get("end_date"),
        )

        db.session.add(new_banner)
        db.session.commit()

        return {
            "id": new_banner.id,
            "club_id": new_banner.club_id,
            "title": new_banner.title,
            "description": new_banner.description,
            "image_url": new_banner.image_url,
            "original_image_url": new_banner.original_image_url,
            "location": new_banner.location,
            "status": new_banner.status,
            "start_date": (
                new_banner.start_date.isoformat() if new_banner.start_date else None
            ),
            "end_date": (
                new_banner.end_date.isoformat() if new_banner.end_date else None
            ),
            "created_at": new_banner.created_at.isoformat(),
            "updated_at": new_banner.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 생성 중 오류 발생: {str(e)}")


def get_banners(status=None, location=None):
    """배너 목록 조회"""
    try:
        query = db.session.query(Banner, Club).join(Club, Banner.club_id == Club.id)

        if status:
            query = query.filter(Banner.status == status)
        if location:
            query = query.filter(Banner.location == location)

        banners = query.order_by(Banner.created_at.desc()).all()

        return [
            {
                "id": banner.id,
                "club_id": banner.club_id,
                "club_name": club.name,
                "title": banner.title,
                "description": banner.description,
                "image_url": banner.image_url,
                "original_image_url": banner.original_image_url,
                "location": banner.location,
                "status": banner.status,
                "start_date": (
                    banner.start_date.isoformat() if banner.start_date else None
                ),
                "end_date": banner.end_date.isoformat() if banner.end_date else None,
                "created_at": banner.created_at.isoformat(),
                "updated_at": banner.updated_at.isoformat(),
            }
            for banner, club in banners
        ]

    except Exception as e:
        raise Exception(f"배너 목록 조회 중 오류 발생: {str(e)}")


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
            "club_name": club.name,
            "title": banner.title,
            "description": banner.description,
            "image_url": banner.image_url,
            "original_image_url": banner.original_image_url,
            "location": banner.location,
            "status": banner.status,
            "start_date": banner.start_date.isoformat() if banner.start_date else None,
            "end_date": banner.end_date.isoformat() if banner.end_date else None,
            "created_at": banner.created_at.isoformat(),
            "updated_at": banner.updated_at.isoformat(),
        }

    except Exception as e:
        raise Exception(f"배너 상세 조회 중 오류 발생: {str(e)}")


def update_banner_status(banner_id, status):
    """배너 상태 변경"""
    try:
        banner = Banner.query.get(banner_id)
        if not banner:
            raise ValueError("해당 배너를 찾을 수 없습니다")

        valid_statuses = ["PENDING", "POSTED", "REJECTED", "EXPIRED"]
        if status not in valid_statuses:
            raise ValueError("유효하지 않은 상태입니다")

        banner.status = status
        db.session.commit()

        return {
            "id": banner.id,
            "club_id": banner.club_id,
            "title": banner.title,
            "status": banner.status,
            "updated_at": banner.updated_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 상태 변경 중 오류 발생: {str(e)}")


def delete_banner(banner_id):
    """배너 삭제"""
    try:
        banner = Banner.query.get(banner_id)
        if not banner:
            raise ValueError("해당 배너를 찾을 수 없습니다")

        # 이미지 파일 삭제 (원본은 최적화 후 삭제되므로 None일 수 있음)
        original_path = None
        if banner.original_image_url:
            original_path = banner.original_image_url.replace("/banners/", "banners/")
        optimized_path = banner.image_url.replace("/banners/", "banners/")
        delete_banner_images(original_path, optimized_path)

        db.session.delete(banner)
        db.session.commit()

        return {"message": "배너가 성공적으로 삭제되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 삭제 중 오류 발생: {str(e)}")

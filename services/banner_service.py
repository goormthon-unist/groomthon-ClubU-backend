from datetime import datetime, date
from typing import List, Dict, Any
from models import Banner, Club, ClubCategory, ClubMember, Role, db
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


def archive_expired_banners():
    """end_date가 지난 배너를 자동으로 ARCHIVED로 변경"""
    try:
        today = date.today()
        expired_banners = Banner.query.filter(
            Banner.end_date < today, Banner.status != "ARCHIVED"
        ).all()

        archived_count = 0
        for banner in expired_banners:
            banner.status = "ARCHIVED"
            archived_count += 1

        if archived_count > 0:
            db.session.commit()

        return archived_count
    except Exception as e:
        db.session.rollback()
        raise Exception(f"배너 자동 아카이브 중 오류 발생: {e}")


def get_banners(status=None, position=None):
    """배너 목록 조회 (POSTED만 반환)"""
    try:
        # 만료된 배너 자동 아카이브 (실시간 체크)
        archive_expired_banners()

        # POSTED 상태만 조회 (ClubCategory join 추가)
        query = (
            db.session.query(Banner, Club, ClubCategory)
            .join(Club, Banner.club_id == Club.id)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
        )
        query = query.filter(Banner.status == "POSTED")

        if position:
            query = query.filter(Banner.position == position)

        banners = query.order_by(Banner.uploaded_at.desc()).all()

        return [
            {
                "id": banner.id,
                "club_id": banner.club_id,
                "user_id": banner.user_id,
                "club_name": club.name,
                "categoryName": category.name,
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
            for banner, club, category in banners
        ]

    except Exception as e:
        raise Exception(f"배너 목록 조회 중 오류 발생: {e}")


def get_all_banners(status=None, position=None):
    """전체 배너 목록 조회 (관리자용)"""
    try:
        # 만료된 배너 자동 아카이브 (실시간 체크)
        archive_expired_banners()

        # ClubCategory join 추가
        query = (
            db.session.query(Banner, Club, ClubCategory)
            .join(Club, Banner.club_id == Club.id)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
        )

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
                "categoryName": category.name,
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
            for banner, club, category in banners
        ]

    except Exception as e:
        raise Exception(f"전체 배너 목록 조회 중 오류 발생: {e}")


def get_banner_by_id(banner_id):
    """배너 상세 조회"""
    try:
        # ClubCategory join 추가
        banner_data = (
            db.session.query(Banner, Club, ClubCategory)
            .join(Club, Banner.club_id == Club.id)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Banner.id == banner_id)
            .first()
        )

        if not banner_data:
            return None

        banner, club, category = banner_data

        return {
            "id": banner.id,
            "club_id": banner.club_id,
            "user_id": banner.user_id,
            "club_name": club.name,
            "categoryName": category.name,
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


def get_banners_by_clubs(club_ids: List[int], user_id: int) -> Dict[str, Any]:
    """
    동아리별 배너 목록 조회

    Args:
        club_ids: 동아리 ID 배열
        user_id: 사용자 ID (권한 확인용)

    Returns:
        {
            "data": {
                "1": [배너 배열],
                "2": [배너 배열],
                ...
            },
            "count": {
                "1": 배너 개수,
                "2": 배너 개수,
                ...
            }
        }
    """
    try:
        # 만료된 배너 자동 아카이브 (실시간 체크)
        archive_expired_banners()

        # 사용자 권한 확인
        from services.permission_service import permission_service

        user_roles = permission_service.get_user_roles(user_id)
        is_admin = "UNION_ADMIN" in user_roles or "DEVELOPER" in user_roles

        # 사용자가 회장인 동아리 목록 조회 (관리자가 아닌 경우)
        accessible_club_ids = set()
        if is_admin:
            # 관리자는 모든 동아리 접근 가능
            accessible_club_ids = set(club_ids)
        else:
            # CLUB_PRESIDENT 권한이 있는 동아리만 접근 가능
            president_memberships = (
                db.session.query(ClubMember, Role)
                .join(Role, ClubMember.role_id == Role.id)
                .filter(
                    ClubMember.user_id == user_id,
                    ClubMember.club_id.in_(club_ids),
                    Role.role_name == "CLUB_PRESIDENT",
                )
                .all()
            )
            accessible_club_ids = {
                member.club_id for member, _ in president_memberships
            }

        # 각 동아리별 배너 조회
        result_data = {}
        result_count = {}

        for club_id in club_ids:
            club_id_str = str(club_id)

            # 권한이 없는 동아리는 빈 배열 반환
            if club_id not in accessible_club_ids:
                result_data[club_id_str] = []
                result_count[club_id_str] = 0
                continue

            # 해당 동아리의 모든 배너 조회 (상태 필터 없이, ClubCategory join 추가)
            banners = (
                db.session.query(Banner, Club, ClubCategory)
                .join(Club, Banner.club_id == Club.id)
                .join(ClubCategory, Club.category_id == ClubCategory.id)
                .filter(Banner.club_id == club_id)
                .order_by(Banner.uploaded_at.desc())
                .all()
            )

            # 배너 데이터 변환
            banner_list = [
                {
                    "id": banner.id,
                    "club_id": banner.club_id,
                    "user_id": banner.user_id,
                    "club_name": club.name,
                    "categoryName": category.name,
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
                for banner, club, category in banners
            ]

            result_data[club_id_str] = banner_list
            result_count[club_id_str] = len(banner_list)

        return {"data": result_data, "count": result_count}

    except Exception as e:
        raise Exception(f"동아리별 배너 조회 중 오류 발생: {e}")

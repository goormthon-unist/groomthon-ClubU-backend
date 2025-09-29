from models import db, NoticeAsset, Notice
from utils.image_utils import (
    save_notice_image,
    save_notice_file,
    delete_notice_asset,
)


def create_notice_asset(notice_id, asset_type, file):
    """공지사항 첨부파일 생성"""
    try:
        # 공지사항 존재 확인
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("존재하지 않는 공지사항입니다")

        # 파일 타입에 따른 처리
        if asset_type == "IMAGE":
            result = save_notice_image(file, notice_id)
        elif asset_type == "FILE":
            result = save_notice_file(file, notice_id)
        else:
            raise ValueError("유효하지 않은 첨부파일 타입입니다")

        # DB에 첨부파일 정보 저장
        notice_asset = NoticeAsset(
            notices_id=notice_id, asset_type=asset_type, file_url=result["file_path"]
        )

        db.session.add(notice_asset)
        db.session.commit()

        return {
            "id": notice_asset.id,
            "notice_id": notice_id,
            "asset_type": asset_type,
            "file_url": result["file_path"],
            "created_at": notice_asset.created_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"첨부파일 생성 중 오류 발생: {e}")


def get_notice_assets(notice_id):
    """공지사항의 모든 첨부파일 조회"""
    try:
        assets = NoticeAsset.query.filter_by(notices_id=notice_id).all()

        return [
            {
                "id": asset.id,
                "notice_id": asset.notices_id,
                "asset_type": asset.asset_type,
                "file_url": asset.file_url,
                "created_at": asset.created_at.isoformat(),
            }
            for asset in assets
        ]

    except Exception as e:
        raise Exception(f"첨부파일 조회 중 오류 발생: {e}")


def delete_notice_asset_by_id(asset_id):
    """공지사항 첨부파일 삭제"""
    try:
        # 첨부파일 조회
        asset = NoticeAsset.query.get(asset_id)
        if not asset:
            raise ValueError("존재하지 않는 첨부파일입니다")

        # 파일 시스템에서 파일 삭제
        file_path = asset.file_url.lstrip("/")  # URL에서 파일 경로 추출
        delete_notice_asset(file_path)

        # DB에서 삭제
        db.session.delete(asset)
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        raise Exception(f"첨부파일 삭제 중 오류 발생: {e}")


def delete_all_notice_assets(notice_id):
    """공지사항의 모든 첨부파일 삭제"""
    try:
        # 공지사항의 모든 첨부파일 조회
        assets = NoticeAsset.query.filter_by(notices_id=notice_id).all()

        for asset in assets:
            # 파일 시스템에서 파일 삭제
            file_path = asset.file_url.lstrip("/")  # URL에서 파일 경로 추출
            delete_notice_asset(file_path)

            # DB에서 삭제
            db.session.delete(asset)

        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        raise Exception(f"첨부파일 일괄 삭제 중 오류 발생: {e}")


def update_notice_asset(asset_id, asset_type, file):
    """공지사항 첨부파일 수정"""
    try:
        # 기존 첨부파일 조회
        asset = NoticeAsset.query.get(asset_id)
        if not asset:
            raise ValueError("존재하지 않는 첨부파일입니다")

        # 기존 파일 삭제
        old_file_path = asset.file_url.lstrip("/")
        delete_notice_asset(old_file_path)

        # 새 파일 저장
        if asset_type == "IMAGE":
            result = save_notice_image(file, asset.notices_id)
        elif asset_type == "FILE":
            result = save_notice_file(file, asset.notices_id)
        else:
            raise ValueError("유효하지 않은 첨부파일 타입입니다")

        # DB 업데이트
        asset.asset_type = asset_type
        asset.file_url = result["file_path"]
        db.session.commit()

        return {
            "id": asset.id,
            "notice_id": asset.notices_id,
            "asset_type": asset.asset_type,
            "file_url": asset.file_url,
            "created_at": asset.created_at.isoformat(),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"첨부파일 수정 중 오류 발생: {e}")

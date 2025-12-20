"""
동아리 관련 서비스
모집 기간 관리 및 D-day 계산
"""

from datetime import date
from models import db, Club


def calculate_recruitment_d_day(recruitment_finish):
    """
    모집 마감일까지의 D-day 계산

    Args:
        recruitment_finish: 모집 마감일 (date 객체 또는 None)

    Returns:
        int: D-day 값
            - 양수: 모집 마감까지 남은 일수
            - 0: 오늘이 모집 마감일
            - 음수: 모집 마감일이 지난 일수
            - None: recruitment_finish가 None인 경우
    """
    if recruitment_finish is None:
        return None

    today = date.today()
    delta = (recruitment_finish - today).days
    return delta


def close_expired_recruitments():
    """recruitment_finish가 지났거나, recruitment_start가 오늘보다 이전인 동아리를 자동으로 CLOSED로 변경"""
    try:
        today = date.today()
        from sqlalchemy import or_, and_

        # 모집 마감일이 지났거나, 모집 시작일이 아직 안 된 경우, 또는 모집기간이 없는 동아리 조회
        expired_clubs = Club.query.filter(
            Club.recruitment_status == "OPEN",
            or_(
                Club.recruitment_finish < today,  # 모집 마감일이 지난 경우
                and_(
                    Club.recruitment_start.isnot(None),
                    today
                    < Club.recruitment_start,  # 모집 시작일이 아직 안 된 경우 (오늘이 모집 시작일보다 이전)
                ),
                Club.recruitment_start.is_(None),  # 모집 시작일이 없는 경우
                Club.recruitment_finish.is_(None),  # 모집 마감일이 없는 경우
            ),
        ).all()

        closed_count = 0
        for club in expired_clubs:
            club.recruitment_status = "CLOSED"
            closed_count += 1

        if closed_count > 0:
            db.session.commit()

        return closed_count
    except Exception as e:
        db.session.rollback()
        raise Exception(f"모집 기간 만료 처리 중 오류 발생: {e}")


def open_started_recruitments():
    """recruitment_start가 오늘이 되는 순간 동아리를 자동으로 OPEN으로 변경"""
    try:
        today = date.today()
        from sqlalchemy import and_, or_

        # 모집 시작일이 오늘이고, 모집 마감일이 지나지 않았으며, 모집기간이 모두 설정된 동아리 조회
        started_clubs = Club.query.filter(
            Club.recruitment_status == "CLOSED",
            Club.recruitment_start == today,  # 모집 시작일이 오늘인 경우
            Club.recruitment_finish >= today,  # 모집 마감일이 오늘이거나 이후인 경우
        ).all()

        opened_count = 0
        for club in started_clubs:
            club.recruitment_status = "OPEN"
            opened_count += 1

        if opened_count > 0:
            db.session.commit()

        return opened_count
    except Exception as e:
        db.session.rollback()
        raise Exception(f"모집 시작 처리 중 오류 발생: {e}")

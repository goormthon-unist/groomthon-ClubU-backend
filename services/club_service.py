"""
동아리 관련 서비스
모집 기간 관리 및 D-day 계산
"""

from datetime import date
from models import db, Club


def calculate_recruitment_d_day(recruitment_start):
    """
    모집 시작일까지의 D-day 계산

    Args:
        recruitment_start: 모집 시작일 (date 객체 또는 None)

    Returns:
        int: D-day 값
            - 양수: 모집 시작까지 남은 일수
            - 0: 오늘이 모집 시작일
            - 음수: 모집 시작일이 지난 일수
            - None: recruitment_start가 None인 경우
    """
    if recruitment_start is None:
        return None

    today = date.today()
    delta = (recruitment_start - today).days
    return delta


def close_expired_recruitments():
    """recruitment_finish가 지난 동아리 또는 모집기간이 없는 동아리를 자동으로 CLOSED로 변경"""
    try:
        today = date.today()
        from sqlalchemy import or_

        # 모집 마감일이 지났거나, 모집기간이 없는 동아리 조회
        expired_clubs = Club.query.filter(
            Club.recruitment_status == "OPEN",
            or_(
                Club.recruitment_finish < today,  # 모집 마감일이 지난 경우
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

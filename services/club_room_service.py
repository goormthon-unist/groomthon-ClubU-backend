from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
from sqlalchemy import and_, or_
from models import db, Room, Reservation, Club, User


class ClubRoomService:
    @staticmethod
    def get_club_remaining_usage(club_id: int, target_date: str) -> Dict:
        """동아리별 사용 가능 시간 조회 (그날/그주)"""
        try:
            # 날짜 파싱
            target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식을 사용해주세요."
            )

        # 해당 동아리가 존재하는지 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"ID {club_id}에 해당하는 동아리를 찾을 수 없습니다.")

        # 해당 날짜의 동아리 예약 조회
        reservations = Reservation.query.filter(
            and_(
                Reservation.club_id == club_id,
                Reservation.date == target_date_obj,
                Reservation.status != "CANCELLED",
            )
        ).all()

        # 해당 주의 시작일과 종료일 계산 (월요일부터 일요일까지)
        week_start = target_date_obj - timedelta(days=target_date_obj.weekday())
        week_end = week_start + timedelta(days=6)

        # 해당 주의 모든 예약 조회
        week_reservations = Reservation.query.filter(
            and_(
                Reservation.club_id == club_id,
                Reservation.date >= week_start,
                Reservation.date <= week_end,
                Reservation.status != "CANCELLED",
            )
        ).all()

        # 그날 사용한 시간 계산
        daily_used_hours = 0
        daily_reservation_details = []

        for reservation in reservations:
            # 시간 차이 계산
            start_datetime = datetime.combine(reservation.date, reservation.start_time)
            end_datetime = datetime.combine(reservation.date, reservation.end_time)
            duration = end_datetime - start_datetime
            used_hours = duration.total_seconds() / 3600  # 시간 단위로 변환

            daily_used_hours += used_hours

            daily_reservation_details.append(
                {
                    "id": reservation.id,
                    "room_name": (
                        reservation.room.name if reservation.room else "알 수 없음"
                    ),
                    "start_time": reservation.start_time.strftime("%H:%M"),
                    "end_time": reservation.end_time.strftime("%H:%M"),
                    "duration_hours": round(used_hours, 1),
                    "status": reservation.status,
                }
            )

        # 그주 사용한 시간 계산
        weekly_used_hours = 0
        weekly_reservation_details = []

        for reservation in week_reservations:
            # 시간 차이 계산
            start_datetime = datetime.combine(reservation.date, reservation.start_time)
            end_datetime = datetime.combine(reservation.date, reservation.end_time)
            duration = end_datetime - start_datetime
            used_hours = duration.total_seconds() / 3600  # 시간 단위로 변환

            weekly_used_hours += used_hours

            weekly_reservation_details.append(
                {
                    "id": reservation.id,
                    "date": reservation.date.strftime("%Y-%m-%d"),
                    "room_name": (
                        reservation.room.name if reservation.room else "알 수 없음"
                    ),
                    "start_time": reservation.start_time.strftime("%H:%M"),
                    "end_time": reservation.end_time.strftime("%H:%M"),
                    "duration_hours": round(used_hours, 1),
                    "status": reservation.status,
                }
            )

        # 제한 시간 설정
        max_daily_hours = 6
        max_weekly_hours = 20  # 주간 최대 사용 시간

        daily_remaining_hours = max(0, max_daily_hours - daily_used_hours)
        weekly_remaining_hours = max(0, max_weekly_hours - weekly_used_hours)

        return {
            "club": {
                "id": club.id,
                "name": club.name,
            },
            "date": target_date,
            "week_range": {
                "start": week_start.strftime("%Y-%m-%d"),
                "end": week_end.strftime("%Y-%m-%d"),
            },
            "daily": {
                "max_hours": max_daily_hours,
                "used_hours": round(daily_used_hours, 1),
                "remaining_hours": round(daily_remaining_hours, 1),
                "reservations": daily_reservation_details,
            },
            "weekly": {
                "max_hours": max_weekly_hours,
                "used_hours": round(weekly_used_hours, 1),
                "remaining_hours": round(weekly_remaining_hours, 1),
                "reservations": weekly_reservation_details,
            },
        }

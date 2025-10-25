from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
from sqlalchemy import and_, or_
from models import db, Room, Reservation, Club, User


class ClubRoomService:
    @staticmethod
    def get_club_remaining_usage(club_id: int, target_date: str) -> Dict:
        """동아리별 사용 가능 시간 조회"""
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

        # 사용한 시간 계산
        total_used_hours = 0
        reservation_details = []

        for reservation in reservations:
            # 시간 차이 계산
            start_datetime = datetime.combine(reservation.date, reservation.start_time)
            end_datetime = datetime.combine(reservation.date, reservation.end_time)
            duration = end_datetime - start_datetime
            used_hours = duration.total_seconds() / 3600  # 시간 단위로 변환

            total_used_hours += used_hours

            reservation_details.append(
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

        # 기본 일일 사용 제한 (예: 6시간)
        max_daily_hours = 6
        remaining_hours = max(0, max_daily_hours - total_used_hours)

        return {
            "club": {
                "id": club.id,
                "name": club.name,
            },
            "date": target_date,
            "max_daily_hours": max_daily_hours,
            "used_hours": round(total_used_hours, 1),
            "remaining_hours": round(remaining_hours, 1),
            "reservations": reservation_details,
        }

from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
from sqlalchemy import and_, or_
from models import db, Room, Reservation, Club, User


class RoomService:
    @staticmethod
    def get_all_rooms() -> List[Dict]:
        """전체 공간 조회"""
        rooms = Room.query.all()
        return [
            {
                "id": room.id,
                "name": room.name,
                "location": room.location,
                "description": room.description,
                "max_daily_hours": room.max_daily_hours,
                "created_at": room.created_at.isoformat() if room.created_at else None,
                "updated_at": room.updated_at.isoformat() if room.updated_at else None,
            }
            for room in rooms
        ]

    @staticmethod
    def get_room_availability(room_id: int, target_date: str) -> Dict:
        """공간별 가용시간 조회"""
        try:
            # 날짜 파싱
            target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식을 사용해주세요."
            )

        # 해당 공간이 존재하는지 확인
        room = Room.query.get(room_id)
        if not room:
            raise ValueError(f"ID {room_id}에 해당하는 공간을 찾을 수 없습니다.")

        # 해당 날짜의 예약 조회
        reservations = Reservation.query.filter(
            and_(
                Reservation.room_id == room_id,
                Reservation.date == target_date_obj,
                Reservation.status != "CANCELLED",  # 취소된 예약은 제외
            )
        ).all()

        # 예약된 시간대 정리
        booked_slots = []
        for reservation in reservations:
            booked_slots.append(
                {
                    "start_time": reservation.start_time.strftime("%H:%M"),
                    "end_time": reservation.end_time.strftime("%H:%M"),
                    "club_name": (
                        reservation.club.name if reservation.club else "알 수 없음"
                    ),
                    "status": reservation.status,
                }
            )

        # 하루 24시간 중 사용 가능한 시간대 계산 (예: 09:00-22:00)
        available_slots = []
        start_hour = 9  # 오전 9시부터
        end_hour = 22  # 오후 10시까지

        for hour in range(start_hour, end_hour):
            slot_start = time(hour, 0)
            slot_end = time(hour + 1, 0)

            # 해당 시간대에 예약이 있는지 확인
            is_booked = False
            for reservation in reservations:
                if (
                    reservation.start_time <= slot_start < reservation.end_time
                    or reservation.start_time < slot_end <= reservation.end_time
                    or (
                        reservation.start_time <= slot_start
                        and reservation.end_time >= slot_end
                    )
                ):
                    is_booked = True
                    break

            if not is_booked:
                available_slots.append(
                    {
                        "start_time": slot_start.strftime("%H:%M"),
                        "end_time": slot_end.strftime("%H:%M"),
                    }
                )

        return {
            "room": {
                "id": room.id,
                "name": room.name,
                "location": room.location,
                "description": room.description,
                "max_daily_hours": room.max_daily_hours,
            },
            "date": target_date,
            "available_slots": available_slots,
            "booked_slots": booked_slots,
        }

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
            "club": {"id": club.id, "name": club.name},
            "date": target_date,
            "max_daily_hours": max_daily_hours,
            "used_hours": round(total_used_hours, 1),
            "remaining_hours": round(remaining_hours, 1),
            "reservations": reservation_details,
        }

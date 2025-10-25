from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
from sqlalchemy import and_, or_
from models import db, Room, Reservation, Club, User


class ReservationService:
    @staticmethod
    def create_reservation(
        club_id: int,
        user_id: int,
        room_id: int,
        date: str,
        start_time: str,
        end_time: str,
        note: Optional[str] = None,
    ) -> Dict:
        """동아리별 대관 신청"""
        try:
            # 날짜와 시간 파싱
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()
        except ValueError as e:
            raise ValueError(f"날짜 또는 시간 형식이 올바르지 않습니다: {str(e)}")

        # 유효성 검증
        if start_time_obj >= end_time_obj:
            raise ValueError("시작 시간은 종료 시간보다 빨라야 합니다.")

        # 해당 동아리, 사용자, 공간이 존재하는지 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"ID {club_id}에 해당하는 동아리를 찾을 수 없습니다.")

        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"ID {user_id}에 해당하는 사용자를 찾을 수 없습니다.")

        room = Room.query.get(room_id)
        if not room:
            raise ValueError(f"ID {room_id}에 해당하는 공간을 찾을 수 없습니다.")

        # 중복 예약 확인
        existing_reservation = Reservation.query.filter(
            and_(
                Reservation.room_id == room_id,
                Reservation.date == date_obj,
                or_(
                    and_(
                        Reservation.start_time <= start_time_obj,
                        Reservation.end_time > start_time_obj,
                    ),
                    and_(
                        Reservation.start_time < end_time_obj,
                        Reservation.end_time >= end_time_obj,
                    ),
                    and_(
                        Reservation.start_time >= start_time_obj,
                        Reservation.end_time <= end_time_obj,
                    ),
                ),
                Reservation.status != "CANCELLED",
            )
        ).first()

        if existing_reservation:
            raise ValueError("해당 시간대에 이미 예약이 있습니다.")

        # 동아리 일일 사용 시간 제한 확인
        club_reservations = Reservation.query.filter(
            and_(
                Reservation.club_id == club_id,
                Reservation.date == date_obj,
                Reservation.status != "CANCELLED",
            )
        ).all()

        # 기존 예약 시간 계산
        total_used_hours = 0
        for reservation in club_reservations:
            start_datetime = datetime.combine(reservation.date, reservation.start_time)
            end_datetime = datetime.combine(reservation.date, reservation.end_time)
            duration = end_datetime - start_datetime
            total_used_hours += duration.total_seconds() / 3600

        # 새 예약 시간 계산
        new_start_datetime = datetime.combine(date_obj, start_time_obj)
        new_end_datetime = datetime.combine(date_obj, end_time_obj)
        new_duration = new_end_datetime - new_start_datetime
        new_hours = new_duration.total_seconds() / 3600

        # 일일 최대 사용 시간 제한 (6시간)
        max_daily_hours = 6
        if total_used_hours + new_hours > max_daily_hours:
            raise ValueError(
                f"일일 최대 사용 시간({max_daily_hours}시간)을 초과합니다. 현재 사용: {total_used_hours:.1f}시간, 신청: {new_hours:.1f}시간"
            )

        # 예약 생성
        reservation = Reservation(
            club_id=club_id,
            user_id=user_id,
            room_id=room_id,
            date=date_obj,
            start_time=start_time_obj,
            end_time=end_time_obj,
            status="CONFIRMED",
            note=note,
        )

        db.session.add(reservation)
        db.session.commit()

        return {
            "id": reservation.id,
            "club": {"id": club.id, "name": club.name},
            "user": {"id": user.id, "name": user.name},
            "room": {"id": room.id, "name": room.name, "location": room.location},
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "duration_hours": round(new_hours, 1),
            "status": reservation.status,
            "note": note,
            "created_at": reservation.created_at.isoformat(),
        }

    @staticmethod
    def get_user_reservations(
        user_id: int, mine: bool = True, status_filter: Optional[List[str]] = None
    ) -> List[Dict]:
        """사용자(나, 동아리) 대관 신청 목록 조회"""
        query = Reservation.query

        if mine:
            # 사용자가 신청한 예약 또는 사용자가 속한 동아리의 예약
            from models import ClubMember
            
            user_clubs = (
                db.session.query(ClubMember.club_id)
                .filter(ClubMember.user_id == user_id)
                .subquery()
            )

            query = query.filter(
                or_(Reservation.user_id == user_id, Reservation.club_id.in_(user_clubs))
            )

        if status_filter:
            query = query.filter(Reservation.status.in_(status_filter))

        reservations = query.order_by(
            Reservation.date.desc(), Reservation.start_time.desc()
        ).all()

        return [
            {
                "id": reservation.id,
                "club": {
                    "id": reservation.club.id if reservation.club else None,
                    "name": reservation.club.name if reservation.club else "알 수 없음",
                },
                "user": {
                    "id": reservation.user.id if reservation.user else None,
                    "name": reservation.user.name if reservation.user else "알 수 없음",
                },
                "room": {
                    "id": reservation.room.id if reservation.room else None,
                    "name": reservation.room.name if reservation.room else "알 수 없음",
                    "location": reservation.room.location if reservation.room else None,
                },
                "date": reservation.date.strftime("%Y-%m-%d"),
                "start_time": reservation.start_time.strftime("%H:%M"),
                "end_time": reservation.end_time.strftime("%H:%M"),
                "status": reservation.status,
                "note": reservation.note,
                "created_at": reservation.created_at.isoformat(),
                "updated_at": reservation.updated_at.isoformat(),
            }
            for reservation in reservations
        ]

    @staticmethod
    def get_reservation_detail(reservation_id: int, user_id: int) -> Dict:
        """예약 상세 조회"""
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 권한 확인: 예약한 사용자이거나 해당 동아리 멤버여야 함
        from models import ClubMember

        is_authorized = (
            reservation.user_id == user_id
            or ClubMember.query.filter(
                and_(
                    ClubMember.user_id == user_id,
                    ClubMember.club_id == reservation.club_id,
                )
            ).first()
            is not None
        )

        if not is_authorized:
            raise ValueError("예약을 조회할 권한이 없습니다.")

        return {
            "id": reservation.id,
            "club": {
                "id": reservation.club.id if reservation.club else None,
                "name": reservation.club.name if reservation.club else "알 수 없음",
                "president_name": (
                    reservation.club.president_name if reservation.club else None
                ),
                "contact": reservation.club.contact if reservation.club else None,
            },
            "user": {
                "id": reservation.user.id if reservation.user else None,
                "name": reservation.user.name if reservation.user else "알 수 없음",
                "email": reservation.user.email if reservation.user else None,
                "phone_number": (
                    reservation.user.phone_number if reservation.user else None
                ),
            },
            "room": {
                "id": reservation.room.id if reservation.room else None,
                "name": reservation.room.name if reservation.room else "알 수 없음",
                "location": reservation.room.location if reservation.room else None,
                "description": (
                    reservation.room.description if reservation.room else None
                ),
            },
            "date": reservation.date.strftime("%Y-%m-%d"),
            "start_time": reservation.start_time.strftime("%H:%M"),
            "end_time": reservation.end_time.strftime("%H:%M"),
            "status": reservation.status,
            "note": reservation.note,
            "created_at": reservation.created_at.isoformat(),
            "updated_at": reservation.updated_at.isoformat(),
        }

    @staticmethod
    def cancel_reservation(reservation_id: int, user_id: int) -> Dict:
        """예약 취소"""
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 권한 확인: 예약한 사용자이거나 해당 동아리 멤버여야 함
        from models import ClubMember

        is_authorized = (
            reservation.user_id == user_id
            or ClubMember.query.filter(
                and_(
                    ClubMember.user_id == user_id,
                    ClubMember.club_id == reservation.club_id,
                )
            ).first()
            is not None
        )

        if not is_authorized:
            raise ValueError("예약을 취소할 권한이 없습니다.")

        # 이미 취소된 예약인지 확인
        if reservation.status == "CANCELLED":
            raise ValueError("이미 취소된 예약입니다.")

        # 예약 취소 (실제로는 삭제하지 않고 상태만 변경)
        reservation.status = "CANCELLED"
        db.session.commit()

        return {
            "id": reservation.id,
            "status": reservation.status,
            "cancelled_at": datetime.utcnow().isoformat(),
            "message": "예약이 성공적으로 취소되었습니다.",
        }

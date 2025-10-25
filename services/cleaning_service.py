from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import and_
from models import db, Reservation, CleaningPhoto, ClubMember
import os
import uuid
from werkzeug.utils import secure_filename


class CleaningService:
    @staticmethod
    def get_usage_detail(reservation_id: int, occurrence_id: int, user_id: int) -> Dict:
        """사용 완료 후 상세 조회"""
        # 예약이 존재하는지 확인
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 권한 확인: 예약한 사용자이거나 해당 동아리 멤버여야 함
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
            raise ValueError("사용 상세를 조회할 권한이 없습니다.")

        # 청소 사진 정보 조회
        cleaning_photos = []
        if reservation.cleaning_photos:
            for photo in reservation.cleaning_photos:
                cleaning_photos.append(
                    {
                        "id": photo.id,
                        "file_url": photo.file_url,
                        "note": photo.note,
                        "created_at": photo.created_at.isoformat(),
                    }
                )

        return {
            "reservation": {
                "id": reservation.id,
                "club": {
                    "id": reservation.club.id if reservation.club else None,
                    "name": reservation.club.name if reservation.club else "알 수 없음",
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
                },
                "date": reservation.date.strftime("%Y-%m-%d"),
                "start_time": reservation.start_time.strftime("%H:%M"),
                "end_time": reservation.end_time.strftime("%H:%M"),
                "status": reservation.status,
                "note": reservation.note,
                "admin_note": reservation.admin_note,
            },
            "occurrence_id": occurrence_id,
            "cleaning_photos": cleaning_photos,
            "submission_status": "PENDING" if cleaning_photos else "NOT_SUBMITTED",
            "submitted_at": (
                cleaning_photos[0]["created_at"] if cleaning_photos else None
            ),
        }

    @staticmethod
    def upload_cleaning_photo(
        reservation_id: int,
        occurrence_id: int,
        file,
        note: Optional[str] = None,
        user_id: int = None,
    ) -> Dict:
        """청소 사진 업로드"""
        # 예약이 존재하는지 확인
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 권한 확인: 예약한 사용자이거나 해당 동아리 멤버여야 함
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
            raise ValueError("청소 사진을 업로드할 권한이 없습니다.")

        # 파일 저장
        if file and file.filename:
            # 파일명 보안 처리
            filename = secure_filename(file.filename)
            # 고유한 파일명 생성
            unique_filename = f"{uuid.uuid4()}_{filename}"

            # 저장 경로 생성: Docker 볼륨 마운트된 경로 사용
            from flask import current_app

            base_dir = current_app.config.get("RESERVATIONS_DIR", "reservations")
            reservation_dir = os.path.join(base_dir, str(reservation_id))
            os.makedirs(reservation_dir, exist_ok=True)

            # 파일 저장
            file_path = os.path.join(reservation_dir, unique_filename)
            file.save(file_path)

            # 파일 URL 생성 (reservations 폴더 기준)
            file_url = f"/{base_dir}/{reservation_id}/{unique_filename}"
        else:
            raise ValueError("파일이 제공되지 않았습니다.")

        # 청소 사진 생성
        cleaning_photo = CleaningPhoto(
            reservation_id=reservation_id,
            file_url=file_url,
            note=note,
        )

        db.session.add(cleaning_photo)
        db.session.commit()

        return {
            "id": cleaning_photo.id,
            "reservation_id": cleaning_photo.reservation_id,
            "file_url": cleaning_photo.file_url,
            "note": cleaning_photo.note,
            "created_at": cleaning_photo.created_at.isoformat(),
        }

    @staticmethod
    def delete_cleaning_photo(
        reservation_id: int, occurrence_id: int, photo_id: int, user_id: int
    ) -> Dict:
        """청소 사진 삭제"""
        # 청소 사진이 존재하는지 확인
        cleaning_photo = CleaningPhoto.query.get(photo_id)
        if not cleaning_photo:
            raise ValueError(f"ID {photo_id}에 해당하는 청소 사진을 찾을 수 없습니다.")

        # 예약 ID 일치 확인
        if cleaning_photo.reservation_id != reservation_id:
            raise ValueError("청소 사진이 해당 예약에 속하지 않습니다.")

        # 권한 확인: 예약한 사용자이거나 해당 동아리 멤버여야 함
        reservation = cleaning_photo.reservation
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
            raise ValueError("청소 사진을 삭제할 권한이 없습니다.")

        # 파일 삭제
        try:
            from flask import current_app

            # file_url에서 실제 파일 경로 추출
            file_path = cleaning_photo.file_url.lstrip("/")

            # Docker 볼륨 마운트된 경로 사용
            base_dir = current_app.config.get("RESERVATIONS_DIR", "reservations")
            if file_path.startswith(base_dir + "/"):
                # 설정된 base_dir 사용
                full_path = os.path.join("/data", file_path)
            else:
                # 기존 방식 (호환성)
                full_path = os.path.join(current_app.root_path, file_path)

            print(f"파일 삭제 시도: {full_path}")

            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"파일 삭제 완료: {full_path}")
            else:
                print(f"파일을 찾을 수 없음: {full_path}")
                # 대안 경로 시도
                alt_path = os.path.join(current_app.root_path, file_path)
                if os.path.exists(alt_path):
                    os.remove(alt_path)
                    print(f"대안 경로에서 파일 삭제 완료: {alt_path}")
                else:
                    print(f"대안 경로에서도 파일을 찾을 수 없음: {alt_path}")
        except Exception as e:
            print(f"파일 삭제 실패: {e}")
            # 파일 삭제 실패해도 DB에서만 삭제

        # 청소 사진 삭제
        db.session.delete(cleaning_photo)
        db.session.commit()

        return {
            "id": photo_id,
            "message": "청소 사진이 성공적으로 삭제되었습니다.",
        }

    @staticmethod
    def get_cleaning_submission_detail(reservation_id: int, occurrence_id: int) -> Dict:
        """청소 사진 제출 상세 조회 (관리자용)"""
        # 예약이 존재하는지 확인
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 청소 사진 정보 조회
        cleaning_photos = []
        if reservation.cleaning_photos:
            for photo in reservation.cleaning_photos:
                cleaning_photos.append(
                    {
                        "id": photo.id,
                        "file_url": photo.file_url,
                        "note": photo.note,
                        "created_at": photo.created_at.isoformat(),
                    }
                )

        return {
            "reservation": {
                "id": reservation.id,
                "club": {
                    "id": reservation.club.id if reservation.club else None,
                    "name": reservation.club.name if reservation.club else "알 수 없음",
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
                },
                "date": reservation.date.strftime("%Y-%m-%d"),
                "start_time": reservation.start_time.strftime("%H:%M"),
                "end_time": reservation.end_time.strftime("%H:%M"),
                "status": reservation.status,
                "note": reservation.note,
                "admin_note": reservation.admin_note,
            },
            "occurrence_id": occurrence_id,
            "cleaning_photos": cleaning_photos,
            "submission_status": "PENDING" if cleaning_photos else "NOT_SUBMITTED",
            "submitted_at": (
                cleaning_photos[0]["created_at"] if cleaning_photos else None
            ),
        }

    @staticmethod
    def approve_cleaning_submission(
        reservation_id: int,
        occurrence_id: int,
        action: str,
        admin_note: Optional[str] = None,
    ) -> Dict:
        """청소 사진 제출 승인/반려"""
        if action not in ["approve", "reject"]:
            raise ValueError("action은 'approve' 또는 'reject'여야 합니다.")

        # 예약이 존재하는지 확인
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            raise ValueError(f"ID {reservation_id}에 해당하는 예약을 찾을 수 없습니다.")

        # 청소 사진이 있는지 확인
        if not reservation.cleaning_photos:
            raise ValueError("제출된 청소 사진이 없습니다.")

        # 예약 상태 및 관리자 메모 업데이트
        if action == "approve":
            reservation.status = "CLEANING_DONE"
            message = "청소 사진이 승인되었습니다."
        else:  # reject
            reservation.status = "CLEANING_REQUIRED"
            message = "청소 사진이 반려되었습니다."

        # admin_note 저장
        if admin_note:
            reservation.admin_note = admin_note

        db.session.commit()

        return {
            "reservation_id": reservation_id,
            "occurrence_id": occurrence_id,
            "action": action,
            "status": reservation.status,
            "admin_note": admin_note,
            "message": message,
            "processed_at": datetime.utcnow().isoformat(),
        }

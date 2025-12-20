from datetime import datetime
from utils.time_utils import get_kst_utcnow

from . import db


class CleaningPhoto(db.Model):
    __tablename__ = "cleaning_photos"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    reservation_id = db.Column(
        db.BigInteger, db.ForeignKey("reservations.id"), nullable=False
    )
    file_url = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=get_kst_utcnow)

    # 관계 설정
    reservation = db.relationship("Reservation", back_populates="cleaning_photos")

    def __repr__(self):
        return f"<CleaningPhoto {self.id} - Reservation {self.reservation_id}>"

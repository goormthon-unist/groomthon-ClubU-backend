from datetime import datetime
from utils.time_utils import get_kst_utcnow

from . import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    club_id = db.Column(db.BigInteger, db.ForeignKey("clubs.id"), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.BigInteger, db.ForeignKey("rooms.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(
        db.Enum("CONFIRMED", "CLEANING_PHOTO_REJECT", "CLEANING_DONE", "CANCELLED"),
        nullable=False,
        default="CONFIRMED",
    )
    is_photo_submitted = db.Column(db.Boolean, nullable=False, default=False)
    note = db.Column(db.Text, nullable=True)
    admin_note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=get_kst_utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=get_kst_utcnow,
        onupdate=get_kst_utcnow,
    )

    # 관계 설정
    club = db.relationship("Club", backref="reservations")
    user = db.relationship("User", backref="reservations")
    room = db.relationship("Room", back_populates="reservations")
    cleaning_photos = db.relationship("CleaningPhoto", back_populates="reservation")

    def __repr__(self):
        return f"<Reservation {self.id} - {self.club.name if self.club else 'Unknown Club'}>"

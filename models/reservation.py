from datetime import datetime

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
        db.Enum("CONFIRMED", "CLEANING_REQUIRED", "CLEANING_DONE"),
        nullable=False,
        default="CONFIRMED",
    )
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # 관계 설정
    club = db.relationship("Club", backref="reservations")
    user = db.relationship("User", backref="reservations")
    room = db.relationship("Room", back_populates="reservations")
    cleaning_photos = db.relationship("CleaningPhoto", back_populates="reservation")

    def __repr__(self):
        return f"<Reservation {self.id} - {self.club.name if self.club else 'Unknown Club'}>"

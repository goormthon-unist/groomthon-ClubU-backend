from datetime import datetime

from . import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    max_daily_hours = db.Column(db.Integer, nullable=False, default=6)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # 관계 설정
    reservations = db.relationship("Reservation", back_populates="room")

    def __repr__(self):
        return f"<Room {self.name}>"

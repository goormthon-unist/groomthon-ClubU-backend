from datetime import datetime

from . import db


class Banner(db.Model):
    __tablename__ = "banners"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    original_image_url = db.Column(db.String(500), nullable=False)
    location = db.Column(
        db.Enum("MAIN_TOP", "MAIN_MIDDLE", "MAIN_BOTTOM", "SIDEBAR"),
        nullable=False,
        default="MAIN_TOP",
    )
    status = db.Column(
        db.Enum("PENDING", "POSTED", "REJECTED", "EXPIRED"),
        nullable=False,
        default="PENDING",
    )
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 관계 설정
    club = db.relationship("Club", backref="banners")

    def __repr__(self):
        return f"<Banner {self.title} (Club {self.club_id})>"

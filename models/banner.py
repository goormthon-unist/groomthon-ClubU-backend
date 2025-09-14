from datetime import datetime

from . import db


class Banner(db.Model):
    __tablename__ = "banners"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    club_id = db.Column(
        db.BigInteger, db.ForeignKey("clubs.id"), nullable=False
    )
    user_id = db.Column(
        db.BigInteger, db.ForeignKey("users.id"), nullable=False
    )
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(
        db.Enum("TOP", "BOTTOM", name="banner_position"),
        nullable=False,
    )
    status = db.Column(
        db.Enum(
            "WAITING", "REJECTED", "POSTED", "ARCHIVED", name="banner_status"
        ),
        nullable=False,
        default="WAITING",
    )
    uploaded_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # 관계 설정
    club = db.relationship("Club", backref="banners")
    user = db.relationship("User", backref="banners")

    def __repr__(self):
        return f"<Banner {self.title} (Club {self.club_id})>"

from datetime import datetime
from utils.time_utils import get_kst_utcnow

from . import db


class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    club_id = db.Column(db.BigInteger, db.ForeignKey("clubs.id"), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=get_kst_utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("POSTED", "DELETE", name="notice_status"),
        nullable=False,
        default="POSTED",
    )
    is_important = db.Column(db.Boolean, nullable=False, default=False)
    views = db.Column(db.BigInteger, nullable=False, default=0)

    # 관계 설정
    club = db.relationship("Club", backref="notices")
    user = db.relationship("User", backref="notices")

    def __repr__(self):
        return f"<Notice {self.title} (Club {self.club_id})>"

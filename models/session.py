from datetime import datetime
from utils.time_utils import get_kst_utcnow
from . import db


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    channel = db.Column(db.String(10), nullable=False)  # WEB, APP
    device_id = db.Column(
        db.String(64), nullable=True
    )  # APP 로그인 시 단말 식별용 UUID (웹은 NULL)
    created_at = db.Column(db.DateTime, nullable=False, default=get_kst_utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # 관계 설정
    user = db.relationship("User", backref="sessions")

    def __repr__(self):
        return (
            f"<UserSession {self.session_id} ({self.channel}) for User {self.user_id}>"
        )

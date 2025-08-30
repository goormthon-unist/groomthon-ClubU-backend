from datetime import datetime
from . import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.BigInteger, primary_key=True)  # ✅ BIGINT
    user_id = db.Column(
        db.BigInteger, db.ForeignKey("users.id"), nullable=False
    )  # ✅ BIGINT
    club_id = db.Column(
        db.BigInteger, db.ForeignKey("clubs.id"), nullable=False
    )  # ✅ BIGINT
    status = db.Column(db.String(20), nullable=False, default="SUBMITTED")
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 동일 유저가 동일 동아리에 중복 지원 방지
    __table_args__ = (
        db.UniqueConstraint("user_id", "club_id", name="uq_applications_user_club"),
    )

    # 관계
    user = db.relationship("User", back_populates="applications")
    club = db.relationship("Club", back_populates="applications")
    answers = db.relationship(
        "ApplicationAnswer",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Application {self.id}:{self.user_id}:{self.club_id}>"

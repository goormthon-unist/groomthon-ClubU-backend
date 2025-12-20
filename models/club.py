from datetime import datetime
from utils.time_utils import get_kst_utcnow

from . import db


class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("club_categories.id"), nullable=False
    )
    activity_summary = db.Column(db.String(255), nullable=True)
    president_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    recruitment_status = db.Column(
        db.Enum("OPEN", "CLOSED"), nullable=False, default="CLOSED"
    )
    current_generation = db.Column(db.Integer, nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    recruitment_start = db.Column(db.Date, nullable=True)
    recruitment_finish = db.Column(db.Date, nullable=True)
    logo_image = db.Column(db.Text, nullable=True)
    introduction_image = db.Column(db.Text, nullable=True)
    club_room = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=get_kst_utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=get_kst_utcnow,
        onupdate=get_kst_utcnow,
    )

    # 관계 설정
    category = db.relationship("ClubCategory", back_populates="clubs")
    members = db.relationship("ClubMember", back_populates="club")
    questions = db.relationship("ClubApplicationQuestion", back_populates="club")
    applications = db.relationship("Application", back_populates="club")

    def __repr__(self):
        return f"<Club {self.name}>"

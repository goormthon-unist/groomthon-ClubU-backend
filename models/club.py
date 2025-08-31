from datetime import datetime

from . import db


class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("club_categories.id"), nullable=False
    )
    activity_summary = db.Column(db.String(255), nullable=True)
    president_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    recruitment_status = db.Column(db.Enum('OPEN', 'CLOSED'), nullable=False, default="CLOSED")
    current_generation = db.Column(db.Integer, nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # 관계 설정
    category = db.relationship("ClubCategory", back_populates="clubs")
    members = db.relationship("ClubMember", back_populates="club")
    questions = db.relationship("ClubApplicationQuestion", back_populates="club")
    applications = db.relationship("Application", back_populates="club")

    def __repr__(self):
        return f"<Club {self.name}>"

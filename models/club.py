from datetime import datetime

from . import db


class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("club_categories.id"), nullable=False
    )
    activity_summary = db.Column(db.String(255))
    president_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    recruitment_status = db.Column(
        db.String(20), nullable=False, default="closed"
    )
    current_generation = db.Column(db.Integer)
    introduction = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # 관계 설정
    category = db.relationship("ClubCategory", back_populates="clubs")
    members = db.relationship("ClubMember", back_populates="club")
    questions = db.relationship(
        "ClubApplicationQuestion", back_populates="club"
    )
    applications = db.relationship("Application", back_populates="club")

    def __repr__(self):
        return f"<Club {self.name}>"

from . import db


class ClubApplicationQuestion(db.Model):
    __tablename__ = "club_application_questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default="text")
    is_required = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    # 관계 설정
    club = db.relationship("Club", back_populates="questions")

    def __repr__(self):
        return f"<ClubApplicationQuestion {self.id}:{self.club_id}>"

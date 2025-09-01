from . import db


class ClubApplicationQuestion(db.Model):
    __tablename__ = "club_application_questions"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    club_id = db.Column(db.BigInteger, db.ForeignKey("clubs.id"), nullable=False)
    question_order = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    # 관계 설정
    club = db.relationship("Club", back_populates="questions")

    def __repr__(self):
        return f"<ClubApplicationQuestion {self.id}:{self.club_id}>"

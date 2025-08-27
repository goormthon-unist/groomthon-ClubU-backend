from . import db


class ApplicationAnswer(db.Model):
    __tablename__ = "application_answers"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("club_application_questions.id"), nullable=False
    )
    answer_text = db.Column(db.Text, nullable=False)

    # 관계 설정
    application = db.relationship("Application", back_populates="answers")
    question = db.relationship("ClubApplicationQuestion")

    def __repr__(self):
        return f"<ApplicationAnswer {self.id}:{self.application_id}>"

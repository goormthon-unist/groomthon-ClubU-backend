from . import db


class ApplicationAnswer(db.Model):
    __tablename__ = "application_answers"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    application_id = db.Column(
        db.BigInteger,
        db.ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,  # ✅ BIGINT
    )
    question_id = db.Column(
        db.BigInteger,
        db.ForeignKey("club_application_questions.id", ondelete="CASCADE"),
        nullable=False,  # ✅ BIGINT
    )
    answer_order = db.Column(db.Integer, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)

    application = db.relationship("Application", back_populates="answers")
    question = db.relationship("ClubApplicationQuestion")  # 필요시 back_populates 추가

    def __repr__(self):
        return f"<ApplicationAnswer {self.id}:{self.application_id}>"

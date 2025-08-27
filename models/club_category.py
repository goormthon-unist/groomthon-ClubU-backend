from . import db


class ClubCategory(db.Model):
    __tablename__ = "club_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    # 관계 설정
    clubs = db.relationship("Club", back_populates="category")

    def __repr__(self):
        return f"<ClubCategory {self.name}>"

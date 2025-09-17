from datetime import datetime

from . import db


class ClubMember(db.Model):
    __tablename__ = "club_members"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    club_id = db.Column(db.BigInteger, db.ForeignKey("clubs.id"), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    generation = db.Column(db.Integer, nullable=False)
    other_info = db.Column(db.Text, nullable=True)
    joined_at = db.Column(db.TIMESTAMP, nullable=False)

    # 관계 설정
    user = db.relationship("User", back_populates="club_members")
    club = db.relationship("Club", back_populates="members")
    role = db.relationship("Role", backref="club_members")  # Role과의 관계 추가

    def __repr__(self):
        return f"<ClubMember {self.user_id}:{self.club_id}>"

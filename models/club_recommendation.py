from datetime import datetime
from utils.time_utils import get_kst_utcnow

from . import db


class ClubRecommendation(db.Model):
    __tablename__ = "club_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=get_kst_utcnow)

    def __repr__(self):
        return f"<ClubRecommendation {self.user_id}:{self.club_id}:{self.score}>"

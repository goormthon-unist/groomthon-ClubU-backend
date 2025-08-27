from . import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = db.relationship('User', back_populates='applications')
    club = db.relationship('Club', back_populates='applications')
    answers = db.relationship('ApplicationAnswer', back_populates='application')
    
    def __repr__(self):
        return f'<Application {self.id}:{self.user_id}:{self.club_id}>'

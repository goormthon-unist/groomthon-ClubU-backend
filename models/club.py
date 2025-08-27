from . import db
from datetime import datetime

class Club(db.Model):
    __tablename__ = 'clubs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('club_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    category = db.relationship('ClubCategory', back_populates='clubs')
    members = db.relationship('ClubMember', back_populates='club')
    questions = db.relationship('ClubApplicationQuestion', back_populates='club')
    applications = db.relationship('Application', back_populates='club')
    
    def __repr__(self):
        return f'<Club {self.name}>'

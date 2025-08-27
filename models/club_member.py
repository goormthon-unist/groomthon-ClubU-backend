from . import db
from datetime import datetime

class ClubMember(db.Model):
    __tablename__ = 'club_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = db.relationship('User', back_populates='club_members')
    club = db.relationship('Club', back_populates='members')
    role = db.relationship('Role')
    
    def __repr__(self):
        return f'<ClubMember {self.user_id}:{self.club_id}>'

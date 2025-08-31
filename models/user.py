from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.Enum('MALE', 'FEMALE', 'OTHER'), nullable=True)
    email_verification_code = db.Column(db.String(10), nullable=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    department = db.relationship("Department", backref="users")
    club_members = db.relationship("ClubMember", back_populates="user")
    applications = db.relationship("Application", back_populates="user")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"

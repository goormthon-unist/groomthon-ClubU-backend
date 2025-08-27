from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 모든 모델들을 여기서 import
from .application import Application
from .application_answer import ApplicationAnswer
from .club import Club
from .club_application_question import ClubApplicationQuestion
from .club_category import ClubCategory
from .club_member import ClubMember
from .club_recommendation import ClubRecommendation
from .department import Department
from .role import Role
from .user import User

__all__ = [
    'db',
    'User',
    'Club', 
    'ClubMember',
    'ClubCategory',
    'ClubApplicationQuestion',
    'Application',
    'ApplicationAnswer',
    'ClubRecommendation',
    'Department',
    'Role'
]

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 모든 모델들을 여기서 import
from .user import User
from .club import Club
from .club_category import ClubCategory
from .club_member import ClubMember
from .club_recommendation import ClubRecommendation
from .club_application_question import ClubApplicationQuestion
from .application import Application
from .application_answer import ApplicationAnswer
from .department import Department
from .role import Role
from .session import UserSession

__all__ = [
    "db",
    "User",
    "Club", 
    "ClubCategory",
    "ClubMember",
    "ClubRecommendation",
    "ClubApplicationQuestion",
    "Application",
    "ApplicationAnswer",
    "Department",
    "Role",
    "UserSession",
]

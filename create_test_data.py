#!/usr/bin/env python3
"""
테스트용 가짜 데이터 생성 스크립트
"""
import os
from datetime import datetime
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# Flask 앱 생성
from app import create_app
from models import db, User, Club, ClubCategory, ClubMember, Role, ClubApplicationQuestion

def create_test_data():
    """테스트용 가짜 데이터 생성"""
    app = create_app()
    
    with app.app_context():
        # 기존 데이터 삭제 (테스트용)
        ClubApplicationQuestion.query.delete()
        ClubMember.query.delete()
        Club.query.delete()
        User.query.delete()
        Role.query.delete()
        ClubCategory.query.delete()
        
        db.session.commit()
        
        print("기존 테스트 데이터 삭제 완료")
        
        # 1. ClubCategory 데이터 생성 (2개)
        categories = [
            ClubCategory(name="학술 분과"),
            ClubCategory(name="문화 분과"),
        ]
        
        for category in categories:
            db.session.add(category)
        db.session.commit()
        print("ClubCategory 데이터 생성 완료")
        
        # 2. User 데이터 생성 (2개)
        users = [
            User(
                name="김철수",
                student_id="2021001",
                email="kim@unist.ac.kr",
                department_id=1
            ),
            User(
                name="이영희", 
                student_id="2021002",
                email="lee@unist.ac.kr",
                department_id=1
            ),
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        print("User 데이터 생성 완료")
        
        # 3. Role 데이터 생성 (2개)
        roles = [
            Role(name="회장"),
            Role(name="부회장"),
        ]
        
        for role in roles:
            db.session.add(role)
        db.session.commit()
        print("Role 데이터 생성 완료")
        
        # 4. Club 데이터 생성 (2개)
        clubs = [
            Club(
                name="Astral",
                category_id=1,
                activity_summary="천체관측 동아리",
                president_name="김철수",
                contact="010-1234-5678",
                recruitment_status="OPEN",
                current_generation=1,
                introduction="천체를 관측하고 우주의 신비를 탐구하는 동아리입니다.",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Club(
                name="Harmony",
                category_id=2,
                activity_summary="음악 동아리",
                president_name="이영희",
                contact="010-9876-5432",
                recruitment_status="CLOSED",
                current_generation=2,
                introduction="다양한 음악을 연주하고 공유하는 동아리입니다.",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
        ]
        
        for club in clubs:
            db.session.add(club)
        db.session.commit()
        print("Club 데이터 생성 완료")
        
        # 5. ClubMember 데이터 생성 (2개)
        members = [
            ClubMember(
                user_id=1,
                club_id=1,
                role_id=1,
                joined_at=datetime.utcnow()
            ),
            ClubMember(
                user_id=2,
                club_id=2,
                role_id=2,
                joined_at=datetime.utcnow()
            ),
        ]
        
        for member in members:
            db.session.add(member)
        db.session.commit()
        print("ClubMember 데이터 생성 완료")
        
        # 6. ClubApplicationQuestion 데이터 생성 (2개)
        questions = [
            ClubApplicationQuestion(
                club_id=1,
                question_text="천체관측에 관심을 가지게 된 계기는 무엇인가요?",
                question_order=1
            ),
            ClubApplicationQuestion(
                club_id=1,
                question_text="우리 동아리에서 하고 싶은 활동은 무엇인가요?",
                question_order=2
            ),
        ]
        
        for question in questions:
            db.session.add(question)
        db.session.commit()
        print("ClubApplicationQuestion 데이터 생성 완료")
        
        print("\n=== 테스트 데이터 생성 완료 ===")
        print("생성된 데이터:")
        print(f"- ClubCategory: {ClubCategory.query.count()}개")
        print(f"- User: {User.query.count()}개")
        print(f"- Role: {Role.query.count()}개")
        print(f"- Club: {Club.query.count()}개")
        print(f"- ClubMember: {ClubMember.query.count()}개")
        print(f"- ClubApplicationQuestion: {ClubApplicationQuestion.query.count()}개")

if __name__ == "__main__":
    create_test_data()

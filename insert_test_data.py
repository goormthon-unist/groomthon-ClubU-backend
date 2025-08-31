from app import create_app
from models import (
    db,
    Role,
    Department,
    User,
    Club,
    ClubCategory,
    ClubMember,
    ClubApplicationQuestion,
    Application,
    ClubRecommendation,
)
from datetime import datetime

app = create_app()
app.app_context().push()

try:
    # 1. Roles
    roles = [
        Role(id=1, name="TEST_회장"),
        Role(id=2, name="TEST_부회장"),
        Role(id=3, name="TEST_일반회원"),
    ]

    for role in roles:
        existing = Role.query.get(role.id)
        if not existing:
            db.session.add(role)

    # 2. Departments
    departments = [
        Department(id=100, name="TEST_컴퓨터공학과", description="TEST_공과대학"),
        Department(id=101, name="TEST_경영학과", description="TEST_경영대학"),
        Department(id=102, name="TEST_디자인학과", description="TEST_디자인대학"),
    ]

    for dept in departments:
        existing = Department.query.get(dept.id)
        if not existing:
            db.session.add(dept)

    # 3. Club Categories
    categories = [
        ClubCategory(id=1, name="학술"),
        ClubCategory(id=2, name="문화"),
        ClubCategory(id=3, name="예술"),
    ]

    for category in categories:
        existing = ClubCategory.query.get(category.id)
        if not existing:
            db.session.add(category)

    # 4. Users
    users = [
        User(
            id=9001,
            name="TEST_김철수",
            email="test_kim@unist.ac.kr",
            student_id="TEST001",
            department_id=100,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        User(
            id=9002,
            name="TEST_이영희",
            email="test_lee@unist.ac.kr",
            student_id="TEST002",
            department_id=101,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        User(
            id=9003,
            name="TEST_박민수",
            email="test_park@unist.ac.kr",
            student_id="TEST003",
            department_id=102,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

    for user in users:
        existing = User.query.get(user.id)
        if not existing:
            db.session.add(user)

    # 5. Clubs
    clubs = [
        Club(
            id=9001,
            name="TEST_코딩클럽2025",
            category_id=1,
            activity_summary="TEST_프로그래밍 스터디 및 해커톤",
            president_name="TEST_김철수",
            contact="test_coding@unist.ac.kr",
            recruitment_status="open",
            introduction="TEST_소개",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Club(
            id=9002,
            name="TEST_뮤직밴드2025",
            category_id=2,
            activity_summary="TEST_록밴드 연주 및 공연",
            president_name="TEST_이영희",
            contact="test_music@unist.ac.kr",
            recruitment_status="closed",
            introduction="TEST_소개",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Club(
            id=9003,
            name="TEST_사진동아리2025",
            category_id=3,
            activity_summary="TEST_포토그래피 및 전시회",
            president_name="TEST_박민수",
            contact="test_photo@unist.ac.kr",
            recruitment_status="open",
            introduction="TEST_소개",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

    for club in clubs:
        existing = Club.query.get(club.id)
        if not existing:
            db.session.add(club)

    # 6. Club Members
    members = [
        ClubMember(
            id=9001,
            user_id=9001,
            club_id=9001,
            role="president",
            joined_at=datetime.now(),
        ),
        ClubMember(
            id=9002,
            user_id=9002,
            club_id=9002,
            role="president",
            joined_at=datetime.now(),
        ),
        ClubMember(
            id=9003,
            user_id=9003,
            club_id=9003,
            role="president",
            joined_at=datetime.now(),
        ),
    ]

    for member in members:
        existing = ClubMember.query.get(member.id)
        if not existing:
            db.session.add(member)

    # 7. Club Application Questions
    questions = [
        ClubApplicationQuestion(
            id=9001, club_id=9001, question_order=1, question_text="TEST_프로그래밍 경험이 있나요?"
        ),
        ClubApplicationQuestion(
            id=9002,
            club_id=9002,
            question_order=1,
            question_text="TEST_악기 연주 경험을 알려주세요",
        ),
        ClubApplicationQuestion(
            id=9003, club_id=9003, question_order=1, question_text="TEST_사진 촬영 경험이 있나요?"
        ),
    ]

    for question in questions:
        existing = ClubApplicationQuestion.query.get(question.id)
        if not existing:
            db.session.add(question)

    # 8. Applications
    applications = [
        Application(
            id=9001,
            user_id=9002,
            club_id=9001,
            status="SUBMITTED",
            submitted_at=datetime.now(),
        ),
        Application(
            id=9002,
            user_id=9003,
            club_id=9002,
            status="VIEWED",
            submitted_at=datetime.now(),
        ),
        Application(
            id=9003,
            user_id=9001,
            club_id=9003,
            status="ACCEPTED",
            submitted_at=datetime.now(),
        ),
    ]

    for application in applications:
        existing = Application.query.get(application.id)
        if not existing:
            db.session.add(application)

    # 9. Club Recommendations
    recommendations = [
        ClubRecommendation(
            id=9001, user_id=9001, club_id=9002, score=0.85, created_at=datetime.now()
        ),
        ClubRecommendation(
            id=9002, user_id=9002, club_id=9003, score=0.90, created_at=datetime.now()
        ),
        ClubRecommendation(
            id=9003, user_id=9003, club_id=9001, score=0.95, created_at=datetime.now()
        ),
    ]

    for recommendation in recommendations:
        existing = ClubRecommendation.query.get(recommendation.id)
        if not existing:
            db.session.add(recommendation)

    db.session.commit()
    print("✅ 모든 테스트 데이터가 성공적으로 추가되었습니다!")

    # 데이터 확인
    print(f"Roles: {Role.query.count()}")
    print(f"Departments: {Department.query.count()}")
    print(f"Users: {User.query.count()}")
    print(f"Clubs: {Club.query.count()}")
    print(f"Applications: {Application.query.count()}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    db.session.rollback()

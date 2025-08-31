from app import create_app
from models import db, Club, ClubCategory, User, Department

app = create_app()
app.app_context().push()

# 테스트 데이터 추가
try:
    # ClubCategory 추가
    categories = [
        ClubCategory(id=1, name="학술", description="학술동아리"),
        ClubCategory(id=2, name="문화", description="문화동아리"),
        ClubCategory(id=3, name="예술", description="예술동아리"),
    ]

    for category in categories:
        existing = ClubCategory.query.get(category.id)
        if not existing:
            db.session.add(category)

    # Department 추가
    departments = [
        Department(id=100, name="컴퓨터공학과", description="공과대학"),
        Department(id=101, name="경영학과", description="경영대학"),
    ]

    for dept in departments:
        existing = Department.query.get(dept.id)
        if not existing:
            db.session.add(dept)

    # Club 추가
    clubs = [
        Club(
            id=9001,
            name="TEST_코딩클럽2025",
            category_id=1,
            activity_summary="프로그래밍 스터디",
            president_name="김철수",
            contact="test@unist.ac.kr",
            recruitment_status="open",
        ),
        Club(
            id=9002,
            name="TEST_뮤직밴드2025",
            category_id=2,
            activity_summary="록밴드 연주",
            president_name="이영희",
            contact="music@unist.ac.kr",
            recruitment_status="closed",
        ),
    ]

    for club in clubs:
        existing = Club.query.get(club.id)
        if not existing:
            db.session.add(club)

    db.session.commit()
    print("테스트 데이터가 성공적으로 추가되었습니다!")

except Exception as e:
    print(f"오류 발생: {e}")
    db.session.rollback()

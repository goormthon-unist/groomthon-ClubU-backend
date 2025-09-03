from models import db, User, Department, ClubMember, Club, ClubCategory, Role
from models import Application, ApplicationAnswer, ClubApplicationQuestion


def get_user_profile(user_id):
    """사용자 프로필 정보 조회 (마이페이지용)"""
    try:
        # 사용자와 학과 정보를 함께 조회
        user_data = (
            db.session.query(User, Department)
            .join(Department, User.department_id == Department.id)
            .filter(User.id == user_id)
            .first()
        )

        if not user_data:
            return None

        user, department = user_data

        # JSON 변환 (비밀번호 제외)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "student_id": user.student_id,
            "phone_number": user.phone_number,
            "gender": user.gender,
            "department": {
                "id": department.id,
                "degree_course": department.degree_course,
                "college": department.college,
                "major": department.major,
            },
            "email_verified": user.email_verified_at is not None,
            "created_at": (
                user.created_at.isoformat() if user.created_at else None
            ),
            "updated_at": (
                user.updated_at.isoformat() if user.updated_at else None
            ),
        }

    except Exception as e:
        raise Exception(f"사용자 프로필 조회 중 오류 발생: {str(e)}")


def get_user_clubs(user_id):
    """사용자가 속한 동아리 목록 조회"""
    try:
        # 사용자가 속한 동아리들과 관련 정보 조회
        clubs_data = (
            db.session.query(ClubMember, Club, ClubCategory, Role)
            .join(Club, ClubMember.club_id == Club.id)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .join(Role, ClubMember.role_id == Role.id)
            .filter(ClubMember.user_id == user_id)
            .all()
        )

        if not clubs_data:
            return []

        # JSON 변환
        return [
            {
                "club": {
                    "id": club.id,
                    "name": club.name,
                    "activity_summary": club.activity_summary,
                    "category": {"id": category.id, "name": category.name},
                    "recruitment_status": club.recruitment_status,
                    "current_generation": club.current_generation,
                    "introduction": club.introduction,
                    "president_name": club.president_name,
                    "contact": club.contact,
                },
                "membership": {
                    "role": {"id": role.id, "name": role.name},
                    "generation": member.generation,
                    "joined_at": (
                        member.joined_at.isoformat() if member.joined_at else None
                    ),
                    "other_info": member.other_info,
                },
            }
            for member, club, category, role in clubs_data
        ]

    except Exception as e:
        raise Exception(f"사용자 동아리 목록 조회 중 오류 발생: {str(e)}")


def get_user_submitted_applications(user_id):
    """사용자의 SUBMITTED 상태 지원서와 답변 조회"""
    try:
        # SUBMITTED 상태의 지원서들과 관련 정보 조회
        applications_data = (
            db.session.query(Application, Club, ClubCategory)
            .join(Club, Application.club_id == Club.id)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Application.user_id == user_id)
            .filter(Application.status == "SUBMITTED")
            .order_by(Application.submitted_at.desc())
            .all()
        )

        if not applications_data:
            return []

        result = []
        for application, club, category in applications_data:
            # 각 지원서의 답변들 조회
            answers_data = (
                db.session.query(ApplicationAnswer, ClubApplicationQuestion)
                .join(
                    ClubApplicationQuestion,
                    ApplicationAnswer.question_id == ClubApplicationQuestion.id,
                )
                .filter(ApplicationAnswer.application_id == application.id)
                .order_by(ApplicationAnswer.answer_order)
                .all()
            )

            # 답변들을 JSON으로 변환
            answers = [
                {
                    "question": {
                        "id": question.id,
                        "question_text": question.question_text,
                        "question_order": question.question_order,
                    },
                    "answer": {
                        "id": answer.id,
                        "answer_text": answer.answer_text,
                        "answer_order": answer.answer_order,
                    },
                }
                for answer, question in answers_data
            ]

            result.append(
                {
                    "application": {
                        "id": application.id,
                        "status": application.status,
                        "submitted_at": (
                            application.submitted_at.isoformat()
                            if application.submitted_at
                            else None
                        ),
                    },
                    "club": {
                        "id": club.id,
                        "name": club.name,
                        "activity_summary": club.activity_summary,
                        "category": {"id": category.id, "name": category.name},
                    },
                    "answers": answers,
                }
            )

        return result

    except Exception as e:
        raise Exception(f"사용자 지원서 조회 중 오류 발생: {str(e)}")

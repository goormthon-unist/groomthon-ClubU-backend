"""
지원서 확인 관련 서비스
"""

from models import (
    db,
    Application,
    ApplicationAnswer,
    User,
    Club,
    Department,
    ClubMember,
    Role,
)
from sqlalchemy.orm import joinedload


def get_club_applicants(club_id):
    """특정 동아리의 지원자 리스트를 조회"""
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}를 찾을 수 없습니다")

        # 해당 동아리의 모든 지원서 조회 (지원자 정보와 함께)
        applications = (
            db.session.query(Application)
            .options(
                joinedload(Application.user).joinedload(User.department),
                joinedload(Application.answers),
            )
            .filter(Application.club_id == club_id)
            .order_by(Application.submitted_at.desc())
            .all()
        )

        if not applications:
            return []

        # 지원자 정보 구성
        applicants = []
        for application in applications:
            user = application.user
            department = user.department

            applicant_info = {
                "application_id": application.id,
                "name": user.name,
                "student_id": user.student_id,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "department": (
                    {
                        "id": department.id,
                        "degree_course": department.degree_course,
                        "college": department.college,
                        "major": department.major,
                    }
                    if department
                    else None
                ),
                "status": application.status,
                "submitted_at": (
                    application.submitted_at.isoformat()
                    if application.submitted_at
                    else None
                ),
            }
            applicants.append(applicant_info)

        return applicants

    except Exception as e:
        raise Exception(f"지원자 목록 조회 중 오류 발생: {str(e)}")


def get_application_detail(application_id):
    """특정 지원서의 상세 정보를 조회"""
    try:
        # 지원서 존재 확인 및 관련 정보 조회
        application = (
            db.session.query(Application)
            .options(
                joinedload(Application.user).joinedload(User.department),
                joinedload(Application.club),
                joinedload(Application.answers).joinedload(ApplicationAnswer.question),
            )
            .filter(Application.id == application_id)
            .first()
        )

        if not application:
            raise ValueError(f"지원서 ID {application_id}를 찾을 수 없습니다")

        user = application.user
        club = application.club
        department = user.department

        # 답변들을 순서대로 정렬
        answers = sorted(application.answers, key=lambda x: x.answer_order)

        application_detail = {
            "application_id": application.id,
            "status": application.status,
            "submitted_at": (
                application.submitted_at.isoformat()
                if application.submitted_at
                else None
            ),
            "user": {
                "id": user.id,
                "name": user.name,
                "student_id": user.student_id,
                "email": user.email,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "department": (
                    {
                        "id": department.id,
                        "degree_course": department.degree_course,
                        "college": department.college,
                        "major": department.major,
                    }
                    if department
                    else None
                ),
            },
            "club": {"id": club.id, "name": club.name},
            "answers": [
                {
                    "id": answer.id,
                    "question_id": answer.question_id,
                    "question_text": (
                        answer.question.question_text if answer.question else None
                    ),
                    "answer_order": answer.answer_order,
                    "answer_text": answer.answer_text,
                }
                for answer in answers
            ],
        }

        return application_detail

    except Exception as e:
        raise Exception(f"지원서 상세 조회 중 오류 발생: {str(e)}")


def register_club_member(
    application_id, role_id=None, generation=None, other_info=None
):
    """지원자를 동아리원으로 등록"""
    try:
        # 지원서 정보 조회
        application = (
            db.session.query(Application)
            .filter(Application.id == application_id)
            .first()
        )
        if not application:
            raise ValueError(f"지원서 ID {application_id}를 찾을 수 없습니다")

        user_id = application.user_id
        club_id = application.club_id

        # 이미 동아리원인지 확인
        existing_member = (
            db.session.query(ClubMember)
            .filter(ClubMember.user_id == user_id, ClubMember.club_id == club_id)
            .first()
        )

        if existing_member:
            raise ValueError("이미 해당 동아리의 회원입니다")

        # 기본값 설정
        if role_id is None:
            # 기본 역할 (일반회원) 찾기
            default_role = (
                db.session.query(Role).filter(Role.name.like("%회원%")).first()
            )
            role_id = default_role.id if default_role else 3  # 일반회원 역할 ID

        if generation is None:
            # 해당 동아리의 현재 기수 사용
            club = db.session.query(Club).filter(Club.id == club_id).first()
            generation = club.current_generation if club.current_generation else 1

        # 동아리원 등록
        from datetime import datetime

        new_member = ClubMember(
            user_id=user_id,
            club_id=club_id,
            role_id=role_id,
            generation=generation,
            other_info=other_info,
            joined_at=datetime.utcnow(),
        )

        db.session.add(new_member)

        # 지원서 상태를 ACCEPTED로 변경
        application.status = "ACCEPTED"

        db.session.commit()

        # 등록된 회원 정보 반환
        member_info = (
            db.session.query(ClubMember, User, Club, Role)
            .join(User, ClubMember.user_id == User.id)
            .join(Club, ClubMember.club_id == Club.id)
            .join(Role, ClubMember.role_id == Role.id)
            .filter(ClubMember.id == new_member.id)
            .first()
        )

        if member_info:
            member, user, club, role = member_info
            return {
                "message": "동아리원 등록이 완료되었습니다",
                "member": {
                    "id": member.id,
                    "user_name": user.name,
                    "student_id": user.student_id,
                    "club_name": club.name,
                    "role_name": role.name,
                    "generation": member.generation,
                    "joined_at": (
                        member.joined_at.isoformat() if member.joined_at else None
                    ),
                },
            }

        return {"message": "동아리원 등록이 완료되었습니다"}

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리원 등록 중 오류 발생: {str(e)}")

"""
관리자 전용 서비스
"""

from datetime import datetime
from models import db, User, Club, ClubMember, Role


def require_admin_user():
    """관리자 권한 확인 (특정 이메일 계정만 허용)"""
    from services.session_service import get_current_user

    current_user = get_current_user()
    if not current_user:
        raise ValueError("로그인이 필요합니다")

    # 관리자 이메일 계정 확인
    admin_emails = ["admin@unist.ac.kr"]  # 환경변수로 설정 가능
    if current_user.email not in admin_emails:
        raise ValueError("관리자 권한이 필요합니다")

    return current_user


def register_club_member_admin(
    user_id, club_id, role_id, generation=None, other_info=None
):
    """관리자가 동아리원을 직접 등록하고 권한 부여"""
    try:
        # 관리자 권한 확인
        require_admin_user()

        # 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}를 찾을 수 없습니다")

        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}를 찾을 수 없습니다")

        # 역할 존재 확인
        role = Role.query.get(role_id)
        if not role:
            raise ValueError(f"역할 ID {role_id}를 찾을 수 없습니다")

        # 이미 동아리원인지 확인
        existing_member = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_member:
            raise ValueError("이미 해당 동아리의 회원입니다")

        # 기본값 설정
        if generation is None:
            generation = club.current_generation if club.current_generation else 1

        # 동아리원 등록
        new_member = ClubMember(
            user_id=user_id,
            club_id=club_id,
            role_id=role_id,
            generation=generation,
            other_info=other_info,
            joined_at=datetime.utcnow(),
        )

        db.session.add(new_member)
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
                    "role_name": role.role_name,
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


def remove_club_member_admin(user_id, club_id):
    """관리자가 동아리원을 탈퇴시킴"""
    try:
        # 관리자 권한 확인
        require_admin_user()

        # 동아리원 멤버십 확인
        membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if not membership:
            raise ValueError("해당 동아리의 회원이 아닙니다")

        # 사용자와 동아리 정보 조회
        user = User.query.get(user_id)
        club = Club.query.get(club_id)

        if not user or not club:
            raise ValueError("사용자 또는 동아리 정보를 찾을 수 없습니다")

        # 탈퇴 처리
        db.session.delete(membership)
        db.session.commit()

        return {
            "message": "동아리원 탈퇴가 완료되었습니다",
            "removed_member": {
                "user_name": user.name,
                "student_id": user.student_id,
                "club_name": club.name,
                "removed_at": datetime.utcnow().isoformat(),
            },
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리원 탈퇴 중 오류 발생: {str(e)}")


def get_available_roles():
    """사용 가능한 역할 목록 조회"""
    try:
        roles = Role.query.all()
        return [
            {
                "id": role.id,
                "role_name": role.role_name,
            }
            for role in roles
        ]
    except Exception as e:
        raise Exception(f"역할 목록 조회 중 오류 발생: {str(e)}")


def get_club_members_admin(club_id):
    """관리자용 동아리원 목록 조회"""
    try:
        # 관리자 권한 확인
        require_admin_user()

        members = (
            db.session.query(ClubMember, User, Club, Role)
            .join(User, ClubMember.user_id == User.id)
            .join(Club, ClubMember.club_id == Club.id)
            .join(Role, ClubMember.role_id == Role.id)
            .filter(ClubMember.club_id == club_id)
            .all()
        )

        member_list = []
        for member, user, club, role in members:
            member_info = {
                "id": member.id,
                "user_name": user.name,
                "student_id": user.student_id,
                "email": user.email,
                "club_name": club.name,
                "role_name": role.role_name,
                "generation": member.generation,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
                "other_info": member.other_info,
            }
            member_list.append(member_info)

        return member_list

    except Exception as e:
        raise Exception(f"동아리원 목록 조회 중 오류 발생: {str(e)}")

"""
동아리 멤버 권한 관리 서비스
동아리 회장이 자신의 동아리 내에서만 멤버 권한을 변경할 수 있도록 제한
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from models import db, User, ClubMember, Role, Club
from config.permission_policy import ROLE_HIERARCHY


def register_club_member(
    club_id: int,
    user_id: int,
    role_name: str,
    generation: Optional[int] = None,
    other_info: Optional[str] = None,
) -> Dict[str, Any]:
    """
    동아리 멤버 직접 등록 (지원서 없이)

    Args:
        club_id: 동아리 ID
        user_id: 사용자 ID
        role_name: 역할명 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT)
        generation: 기수 (선택사항)
        other_info: 기타 정보 (선택사항)

    Returns:
        Dict with success status and data
    """
    try:
        # 1. 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}가 존재하지 않습니다.")

        # 2. 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}가 존재하지 않습니다.")

        # 3. 역할 존재 확인 (동아리 내 역할만 허용)
        allowed_roles = ["CLUB_MEMBER", "CLUB_OFFICER", "CLUB_PRESIDENT"]
        if role_name not in allowed_roles:
            raise ValueError(
                f"동아리 내에서 허용되지 않는 역할입니다. 허용된 역할: {', '.join(allowed_roles)}"
            )

        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            raise ValueError(f"역할 '{role_name}'이 존재하지 않습니다.")

        # 4. 이미 동아리 멤버인지 확인
        existing_membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_membership:
            raise ValueError("이미 해당 동아리의 회원입니다.")

        # 5. 기본값 설정
        if generation is None:
            generation = club.current_generation if club.current_generation else 1

        # 6. 동아리 멤버 등록
        new_membership = ClubMember(
            user_id=user_id,
            club_id=club_id,
            role_id=role.id,
            generation=generation,
            other_info=other_info,
            joined_at=datetime.utcnow(),
        )

        db.session.add(new_membership)
        db.session.commit()

        return {
            "success": True,
            "message": f"사용자 {user.name}을(를) {club.name} 동아리의 {role_name}으로 등록했습니다.",
            "data": {
                "membership_id": new_membership.id,
                "user_id": user_id,
                "club_id": club_id,
                "role_name": role_name,
                "generation": generation,
                "joined_at": new_membership.joined_at.isoformat(),
            },
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 멤버 등록 중 오류 발생: {str(e)}")


def change_club_member_role(
    club_id: int,
    user_id: int,
    role_name: str,
    generation: Optional[int] = None,
    other_info: Optional[str] = None,
) -> Dict[str, Any]:
    """
    동아리 내 멤버 권한 변경

    Args:
        club_id: 동아리 ID
        user_id: 사용자 ID
        role_name: 변경할 역할명 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT)
        generation: 기수 (선택사항)
        other_info: 기타 정보 (선택사항)

    Returns:
        Dict with success status and data
    """
    try:
        # 1. 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}가 존재하지 않습니다.")

        # 2. 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}가 존재하지 않습니다.")

        # 3. 역할 존재 확인 (동아리 내 역할만 허용)
        allowed_roles = ["CLUB_MEMBER", "CLUB_OFFICER", "CLUB_PRESIDENT"]
        if role_name not in allowed_roles:
            raise ValueError(
                f"동아리 내에서 허용되지 않는 역할입니다. 허용된 역할: {', '.join(allowed_roles)}"
            )

        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            raise ValueError(f"역할 '{role_name}'이 존재하지 않습니다.")

        # 4. 기존 동아리 멤버십 확인
        existing_membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_membership:
            # 기존 멤버십 업데이트
            existing_membership.role_id = role.id
            if generation is not None:
                existing_membership.generation = generation
            if other_info is not None:
                existing_membership.other_info = other_info
            existing_membership.updated_at = datetime.utcnow()

            db.session.commit()

            return {
                "success": True,
                "message": f"동아리 멤버 권한이 '{role_name}'으로 변경되었습니다.",
                "data": {
                    "user_id": user_id,
                    "user_name": user.name,
                    "club_id": club_id,
                    "club_name": club.name,
                    "role_name": role_name,
                    "generation": existing_membership.generation,
                    "other_info": existing_membership.other_info,
                    "updated_at": existing_membership.updated_at.isoformat(),
                },
            }
        else:
            # 새 멤버십 생성
            new_membership = ClubMember(
                user_id=user_id,
                club_id=club_id,
                role_id=role.id,
                generation=generation or 1,
                other_info=other_info,
                joined_at=datetime.utcnow(),
            )

            db.session.add(new_membership)
            db.session.commit()

            return {
                "success": True,
                "message": f"사용자가 동아리에 '{role_name}'으로 추가되었습니다.",
                "data": {
                    "user_id": user_id,
                    "user_name": user.name,
                    "club_id": club_id,
                    "club_name": club.name,
                    "role_name": role_name,
                    "generation": new_membership.generation,
                    "other_info": new_membership.other_info,
                    "joined_at": new_membership.joined_at.isoformat(),
                },
            }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 멤버 권한 변경 중 오류 발생: {str(e)}")


def get_club_member_roles(club_id: int, user_id: int) -> Dict[str, Any]:
    """
    동아리 내 특정 사용자의 역할 조회

    Args:
        club_id: 동아리 ID
        user_id: 사용자 ID

    Returns:
        Dict with user roles in the club
    """
    try:
        # 1. 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}가 존재하지 않습니다.")

        # 2. 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}가 존재하지 않습니다.")

        # 3. 동아리 내 멤버십 조회
        membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if not membership:
            return {
                "success": True,
                "message": "해당 사용자는 이 동아리의 멤버가 아닙니다.",
                "data": {
                    "user_id": user_id,
                    "user_name": user.name,
                    "club_id": club_id,
                    "club_name": club.name,
                    "role_name": None,
                    "is_member": False,
                },
            }

        role = Role.query.get(membership.role_id)

        return {
            "success": True,
            "message": "동아리 멤버 정보를 조회했습니다.",
            "data": {
                "user_id": user_id,
                "user_name": user.name,
                "club_id": club_id,
                "club_name": club.name,
                "role_name": role.role_name if role else None,
                "generation": membership.generation,
                "other_info": membership.other_info,
                "joined_at": membership.joined_at.isoformat(),
                "is_member": True,
            },
        }

    except Exception as e:
        raise Exception(f"동아리 멤버 정보 조회 중 오류 발생: {str(e)}")


def get_club_available_roles() -> Dict[str, Any]:
    """
    동아리 내에서 사용 가능한 역할 목록 조회

    Returns:
        Dict with available roles for club management
    """
    try:
        # 동아리 내에서 사용 가능한 역할들
        allowed_roles = ["CLUB_MEMBER", "CLUB_OFFICER", "CLUB_PRESIDENT"]

        roles = Role.query.filter(Role.role_name.in_(allowed_roles)).all()

        role_list = []
        for role in roles:
            role_list.append(
                {
                    "role_id": role.id,
                    "role_name": role.role_name,
                    "description": _get_role_description(role.role_name),
                }
            )

        return {
            "success": True,
            "message": "동아리 내 사용 가능한 역할 목록을 조회했습니다.",
            "data": {"roles": role_list, "total_count": len(role_list)},
        }

    except Exception as e:
        raise Exception(f"동아리 역할 목록 조회 중 오류 발생: {str(e)}")


def get_club_members_list(club_id: int) -> Dict[str, Any]:
    """
    동아리 멤버 목록 조회 (권한별 정렬)

    Args:
        club_id: 동아리 ID

    Returns:
        Dict with club members list
    """
    try:
        # 1. 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}가 존재하지 않습니다.")

        # 2. 동아리 멤버 목록 조회 (권한별 정렬)
        memberships = (
            ClubMember.query.filter_by(club_id=club_id)
            .join(User, ClubMember.user_id == User.id)
            .join(Role, ClubMember.role_id == Role.id)
            .order_by(
                Role.id.desc(),  # 권한 높은 순 (CLUB_PRESIDENT → CLUB_OFFICER → CLUB_MEMBER)
                User.name.asc(),  # 이름순
            )
            .all()
        )

        member_list = []
        for membership in memberships:
            user = membership.user
            role = Role.query.get(membership.role_id)

            member_list.append(
                {
                    "user_id": user.id,
                    "user_name": user.name,
                    "user_email": user.email,
                    "student_id": user.student_id,
                    "role_id": role.id,
                    "role_name": role.role_name,
                    "role_description": _get_role_description(role.role_name),
                    "generation": membership.generation,
                    "other_info": membership.other_info,
                    "joined_at": membership.joined_at.isoformat(),
                }
            )

        return {
            "success": True,
            "message": f"동아리 '{club.name}' 멤버 목록을 조회했습니다.",
            "data": {
                "club_id": club_id,
                "club_name": club.name,
                "members": member_list,
                "total_count": len(member_list),
            },
        }

    except Exception as e:
        raise Exception(f"동아리 멤버 목록 조회 중 오류 발생: {str(e)}")


def _get_role_description(role_name: str) -> str:
    """역할 설명 반환"""
    descriptions = {
        "CLUB_MEMBER": "동아리 일반 멤버",
        "CLUB_OFFICER": "동아리 임원",
        "CLUB_PRESIDENT": "동아리 회장",
    }
    return descriptions.get(role_name, "알 수 없는 역할")

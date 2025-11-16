"""
동아리 멤버 권한 관리 서비스
동아리 회장이 자신의 동아리 내에서만 멤버 권한을 변경할 수 있도록 제한
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from models import db, User, ClubMember, Role, Club
from config.permission_policy import ROLE_HIERARCHY
from .user_search_service import find_user_by_student_id_and_name


def register_club_member_improved(
    club_id: int,
    student_id: str,
    name: str,
    role_name: str,
    generation: Optional[int] = None,
    other_info: Optional[str] = None,
) -> Dict[str, Any]:
    """
    개선된 동아리 멤버 등록 (학번과 이름으로 검색)

    Args:
        club_id: 동아리 ID
        student_id: 학번
        name: 이름
        role_name: 역할명 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT, CLUB_INACTIVE)
        generation: 기수 (선택사항)
        other_info: 기타 정보 (선택사항)

    Returns:
        Dict with success status and data
    """
    try:
        # 1. 사용자 검색 및 검증
        user_search_result = find_user_by_student_id_and_name(student_id, name)
        user_id = user_search_result["user_id"]
        user_name = user_search_result["name"]

        # 2. 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError(f"동아리 ID {club_id}가 존재하지 않습니다.")

        # 3. 역할 존재 확인 (휴동중 포함)
        allowed_roles = [
            "CLUB_MEMBER",
            "CLUB_OFFICER",
            "CLUB_PRESIDENT",
            "CLUB_MEMBER_REST",
            "STUDENT",
        ]
        if role_name not in allowed_roles:
            raise ValueError(
                f"동아리 내에서 허용되지 않는 역할입니다. 허용된 역할: {', '.join(allowed_roles)}"
            )

        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            raise ValueError(f"역할 '{role_name}'이 존재하지 않습니다.")

        # 4. 기존 멤버십 확인
        existing_membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_membership:
            # 기존 역할 확인
            existing_role = Role.query.get(existing_membership.role_id)
            existing_role_name = existing_role.role_name if existing_role else None

            # 같은 역할로 재등록 시도 시 에러
            if existing_role_name == role_name and role_name != "STUDENT":
                raise ValueError(
                    f"사용자 {user_name}({student_id})은(는) 이미 {club.name} 동아리의 {role_name}으로 등록되어 있습니다."
                )

            if role_name == "STUDENT":
                # STUDENT로 설정 시 해당 동아리에서 완전히 제거
                # 전역 STUDENT 역할은 이미 존재하므로 별도 처리 불필요
                db.session.delete(existing_membership)
                db.session.commit()
                message = f"사용자 {user_name}({student_id})이(가) {club.name} 동아리에서 탈퇴되었습니다."
            else:
                # 기존 멤버십 업데이트 (역할 변경, 휴동중에서 복귀 등)
                existing_membership.role_id = role.id
                if generation is not None:
                    existing_membership.generation = generation
                if other_info is not None:
                    existing_membership.other_info = other_info
                existing_membership.updated_at = datetime.utcnow()

                db.session.commit()

                if existing_role_name != role_name:
                    message = f"사용자 {user_name}({student_id})의 동아리 역할이 '{existing_role_name}'에서 '{role_name}'으로 변경되었습니다."
                else:
                    message = f"사용자 {user_name}({student_id})의 동아리 정보가 업데이트되었습니다."
        else:
            if role_name == "STUDENT":
                # STUDENT로 설정 시 이미 탈퇴 상태
                # 전역 STUDENT 역할은 이미 존재하므로 별도 처리 불필요
                message = f"사용자 {user_name}({student_id})은(는) 이미 {club.name} 동아리에서 탈퇴한 상태입니다."
            else:
                # 새 멤버십 생성
                if generation is None:
                    generation = (
                        club.current_generation if club.current_generation else 1
                    )

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

                message = f"사용자 {user_name}({student_id})을(를) {club.name} 동아리의 {role_name}으로 등록했습니다."

        # 간소화된 응답
        return {
            "success": True,
            "message": message,
            "data": {
                "user_id": user_id,
                "name": user_name,
                "student_id": student_id,
                "role_name": role_name,
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
        allowed_roles = [
            "CLUB_MEMBER",
            "CLUB_OFFICER",
            "CLUB_PRESIDENT",
            "CLUB_MEMBER_REST",
            "STUDENT",
        ]
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
            if role_name == "STUDENT":
                # STUDENT로 설정 시 해당 동아리에서 완전히 제거
                # 전역 STUDENT 역할은 이미 존재하므로 별도 처리 불필요
                db.session.delete(existing_membership)
                db.session.commit()

                return {
                    "success": True,
                    "message": f"동아리 멤버가 '{role_name}'으로 변경되어 {club.name} 동아리에서 탈퇴되었습니다.",
                    "data": {
                        "user_id": user_id,
                        "user_name": user.name,
                        "club_id": club_id,
                        "club_name": club.name,
                        "role_name": role_name,
                        "generation": None,
                        "other_info": other_info,
                        "updated_at": datetime.utcnow().isoformat(),
                    },
                }
            else:
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
            if role_name == "STUDENT":
                # STUDENT로 설정 시 이미 탈퇴 상태
                # 전역 STUDENT 역할은 이미 존재하므로 별도 처리 불필요
                return {
                    "success": True,
                    "message": f"사용자는 이미 {club.name} 동아리에서 탈퇴한 상태입니다.",
                    "data": {
                        "user_id": user_id,
                        "user_name": user.name,
                        "club_id": club_id,
                        "club_name": club.name,
                        "role_name": role_name,
                        "generation": None,
                        "other_info": other_info,
                        "joined_at": None,
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
        # 동아리 내에서 사용 가능한 역할들 (휴동중 포함)
        allowed_roles = [
            "CLUB_MEMBER",
            "CLUB_OFFICER",
            "CLUB_PRESIDENT",
            "CLUB_MEMBER_REST",
            "STUDENT",
        ]

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
        "CLUB_MEMBER_REST": "동아리 휴동중",
        "STUDENT": "일반 학생 (탈퇴)",
    }
    return descriptions.get(role_name, "알 수 없는 역할")

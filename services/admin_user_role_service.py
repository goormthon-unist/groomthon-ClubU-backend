"""
관리자용 사용자 권한 변경 서비스
DEVELOPER 권한을 가진 관리자만 사용자 권한을 변경할 수 있음
"""

from datetime import datetime
from models import db, User, Club, ClubMember, Role
from services.permission_service import permission_service
from utils.time_utils import get_kst_now_naive


def change_user_role(user_id, club_id, new_role_name, generation=None, other_info=None):
    """
    사용자의 동아리 내 권한을 변경

    Args:
        user_id: 사용자 ID
        club_id: 동아리 ID (None이면 전역 권한)
        new_role_name: 새로운 역할명 (예: 'CLUB_PRESIDENT', 'CLUB_MEMBER')
        generation: 기수 (선택사항)
        other_info: 기타 정보 (선택사항)

    Returns:
        Dict: 변경 결과 정보
    """
    try:
        # 1. 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}를 찾을 수 없습니다")

        # 2. 동아리 존재 확인 (club_id가 None이 아닌 경우)
        if club_id is not None:
            club = Club.query.get(club_id)
            if not club:
                raise ValueError(f"동아리 ID {club_id}를 찾을 수 없습니다")

        # 3. 역할 존재 확인
        role = Role.query.filter_by(role_name=new_role_name).first()
        if not role:
            raise ValueError(f"역할 '{new_role_name}'을 찾을 수 없습니다")

        # 4. 기존 멤버십 조회
        existing_membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_membership:
            # 5. 기존 멤버십 업데이트
            existing_membership.role_id = role.id
            if generation is not None:
                existing_membership.generation = generation
            if other_info is not None:
                existing_membership.other_info = other_info
            existing_membership.joined_at = (
                get_kst_now_naive()
            )  # 권한 변경 시간으로 업데이트

            db.session.commit()

            # 권한 캐시 삭제
            permission_service.clear_user_cache(user_id)

            return {
                "success": True,
                "message": f"사용자 {user.name}의 권한이 '{new_role_name}'으로 변경되었습니다",
                "data": {
                    "user_id": user_id,
                    "user_name": user.name,
                    "club_id": club_id,
                    "club_name": club.name if club else "전역",
                    "old_role": (
                        existing_membership.role.role_name
                        if existing_membership.role
                        else None
                    ),
                    "new_role": new_role_name,
                    "generation": existing_membership.generation,
                    "changed_at": existing_membership.joined_at.isoformat(),
                },
            }
        else:
            # 6. 새로운 멤버십 생성
            new_membership = ClubMember(
                user_id=user_id,
                club_id=club_id,
                role_id=role.id,
                generation=generation or 1,
                other_info=other_info,
                joined_at=get_kst_now_naive(),
            )

            db.session.add(new_membership)
            db.session.commit()

            # 권한 캐시 삭제
            permission_service.clear_user_cache(user_id)

            return {
                "success": True,
                "message": f"사용자 {user.name}에게 '{new_role_name}' 권한이 부여되었습니다",
                "data": {
                    "user_id": user_id,
                    "user_name": user.name,
                    "club_id": club_id,
                    "club_name": club.name if club else "전역",
                    "old_role": None,
                    "new_role": new_role_name,
                    "generation": new_membership.generation,
                    "changed_at": new_membership.joined_at.isoformat(),
                },
            }

    except ValueError as ve:
        # 비즈니스 로직 오류는 그대로 전달
        raise ve
    except Exception as e:
        db.session.rollback()
        raise Exception(f"사용자 권한 변경 중 오류 발생: {str(e)}")


def get_user_roles(user_id):
    """
    사용자의 모든 권한 조회

    Args:
        user_id: 사용자 ID

    Returns:
        Dict: 사용자의 모든 권한 정보
    """
    try:
        # 1. 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"사용자 ID {user_id}를 찾을 수 없습니다")

        # 2. 사용자의 모든 멤버십 조회
        memberships = (
            db.session.query(ClubMember, Role, Club)
            .outerjoin(Role, ClubMember.role_id == Role.id)
            .outerjoin(Club, ClubMember.club_id == Club.id)
            .filter(ClubMember.user_id == user_id)
            .all()
        )

        roles = []
        for membership, role, club in memberships:
            roles.append(
                {
                    "club_id": membership.club_id,
                    "club_name": club.name if club else "전역",
                    "role_name": role.role_name if role else "UNKNOWN",
                    "generation": membership.generation,
                    "other_info": membership.other_info,
                    "joined_at": (
                        membership.joined_at.isoformat()
                        if membership.joined_at
                        else None
                    ),
                }
            )

        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "user_name": user.name,
                "user_email": user.email,
                "roles": roles,
                "total_roles": len(roles),
            },
        }

    except ValueError as ve:
        # 비즈니스 로직 오류는 그대로 전달
        raise ve
    except Exception as e:
        raise Exception(f"사용자 권한 조회 중 오류 발생: {str(e)}")


def get_available_roles():
    """
    사용 가능한 모든 역할 조회

    Returns:
        Dict: 사용 가능한 역할 목록
    """
    try:
        roles = Role.query.all()

        role_list = []
        for role in roles:
            role_list.append(
                {
                    "id": role.id,
                    "role_name": role.role_name,
                    "description": f"{role.role_name} 권한",
                }
            )

        return {
            "success": True,
            "data": {"roles": role_list, "total_roles": len(role_list)},
        }

    except Exception as e:
        raise Exception(f"역할 목록 조회 중 오류 발생: {str(e)}")

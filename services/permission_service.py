"""
권한 검사 서비스 클래스
실질적인 권한 검사 로직을 캡슐화하여 테스트/재사용 용이
"""

from typing import Set, Optional, Dict, Any
from flask import current_app
from models import db, User, ClubMember, Role
from config.permission_policy import (
    get_permission_policy,
    ROLE_HIERARCHY,
    CLUB_SCOPED_PERMISSIONS,
)


class PermissionService:
    """권한 검사 서비스"""

    def __init__(self):
        self._user_roles_cache = {}  # 간단한 메모리 캐시

    def check_permission(
        self,
        permission_key: str,
        user_id: Optional[int] = None,
        club_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        권한 검사 메인 메서드

        Args:
            permission_key: 권한 키 (예: 'clubs.update')
            user_id: 사용자 ID (None이면 현재 세션 사용자)
            club_id: 동아리 ID (특정 동아리 컨텍스트에서 권한 검사)

        Returns:
            Dict with keys: has_permission, message, user_id, user_roles, required_roles, club_id
        """
        try:
            # 1. 권한 정책 조회
            policy = get_permission_policy(permission_key)
            if not policy:
                # 권한 정책이 없는 경우 기본 'STUDENT' 권한 필요
                required_roles = {"STUDENT"}
            else:
                required_roles = policy["allowed_roles"]
                # 빈 집합인 경우 기본 'STUDENT' 권한 필요
                if not required_roles:
                    required_roles = {"STUDENT"}

            # 2. club 스코프 필수 권한인데 club_id가 없는 경우 즉시 거절
            if permission_key in CLUB_SCOPED_PERMISSIONS and club_id is None:
                return {
                    "has_permission": False,
                    "message": "club_id가 필요합니다",
                    "user_id": user_id,
                    "user_roles": set(),
                    "required_roles": required_roles,
                    "club_id": club_id,
                }

            # 3. 사용자 ID 확인
            if user_id is None:
                from services.session_service import get_current_user

                current_user = get_current_user()
                if not current_user:
                    return {
                        "has_permission": False,
                        "message": "로그인이 필요합니다",
                        "user_id": None,
                        "user_roles": set(),
                        "required_roles": required_roles,
                    }
                user_id = current_user.id

            # 4. 사용자 권한 조회 (동아리 컨텍스트 고려)
            if club_id is not None:
                # 특정 동아리 컨텍스트에서 권한 검사
                user_roles = self.get_user_roles_in_club(user_id, club_id)
            else:
                # 전역 권한 검사
                user_roles = self.get_user_roles(user_id)

            # 5. 권한 검사
            has_permission = bool(user_roles.intersection(required_roles))

            if has_permission:
                message = (
                    f'권한 확인됨: {", ".join(user_roles.intersection(required_roles))}'
                )
            else:
                message = f'권한 부족. 필요: {", ".join(required_roles)}, 현재: {", ".join(user_roles) if user_roles else "없음"}'

            return {
                "has_permission": has_permission,
                "message": message,
                "user_id": user_id,
                "user_roles": user_roles,
                "required_roles": required_roles,
                "club_id": club_id,
            }

        except Exception as e:
            current_app.logger.exception(f"권한 검사 중 오류 발생: {permission_key}")
            return {
                "has_permission": False,
                "message": f"권한 검사 중 오류 발생: {str(e)}",
                "user_id": user_id,
                "user_roles": set(),
                "required_roles": set(),
                "club_id": club_id,
            }

    def get_user_roles(self, user_id: int) -> Set[str]:
        """
        사용자의 모든 권한 조회 (전역 + 클럽별)

        Args:
            user_id: 사용자 ID

        Returns:
            사용자가 가진 모든 역할명의 집합
        """
        try:
            # 캐시 확인
            cache_key = f"user_roles_{user_id}"
            if cache_key in self._user_roles_cache:
                return self._user_roles_cache[cache_key]

            # DB에서 사용자 권한 조회
            memberships = (
                db.session.query(ClubMember, Role)
                .join(Role, ClubMember.role_id == Role.id)
                .filter(ClubMember.user_id == user_id)
                .all()
            )

            user_roles = set()
            for membership, role in memberships:
                user_roles.add(role.role_name)

            # 캐시 저장 (간단한 메모리 캐시, 실제로는 Redis 등 사용 권장)
            self._user_roles_cache[cache_key] = user_roles

            return user_roles

        except Exception as e:
            current_app.logger.exception(
                f"사용자 권한 조회 중 오류 발생: user_id={user_id}"
            )
            return set()

    def get_user_club_roles(self, user_id: int, club_id: int) -> Set[str]:
        """
        특정 클럽에서의 사용자 권한 조회

        Args:
            user_id: 사용자 ID
            club_id: 클럽 ID

        Returns:
            해당 클럽에서의 역할명 집합
        """
        try:
            memberships = (
                db.session.query(ClubMember, Role)
                .join(Role, ClubMember.role_id == Role.id)
                .filter(ClubMember.user_id == user_id, ClubMember.club_id == club_id)
                .all()
            )

            club_roles = {role.role_name for _, role in memberships}

            # 디버깅 로그 추가
            if not club_roles:
                current_app.logger.warning(
                    f"클럽 권한 조회 결과 없음: user_id={user_id}, club_id={club_id}, "
                    f"조회된 멤버십 수: {len(memberships)}"
                )
            else:
                current_app.logger.debug(
                    f"클럽 권한 조회 성공: user_id={user_id}, club_id={club_id}, "
                    f"권한: {club_roles}"
                )

            return club_roles

        except Exception as e:
            current_app.logger.exception(
                f"클럽 권한 조회 중 오류 발생: user_id={user_id}, club_id={club_id}"
            )
            return set()

    def get_user_roles_in_club(self, user_id: int, club_id: int) -> Set[str]:
        """
        특정 동아리에서의 사용자 권한 조회 (전역 권한 + 동아리 권한)

        Args:
            user_id: 사용자 ID
            club_id: 동아리 ID

        Returns:
            해당 동아리에서 유효한 모든 권한 (전역 + 동아리별)
        """
        try:
            # 1. 전역 권한 조회
            global_roles = self.get_user_global_roles(user_id)

            # 2. 해당 동아리 권한 조회
            club_roles = self.get_user_club_roles(user_id, club_id)

            # 3. 전역 권한과 동아리 권한 합치기
            all_roles = global_roles.union(club_roles)

            # 디버깅 로그 추가
            current_app.logger.debug(
                f"동아리 컨텍스트 권한 조회: user_id={user_id}, club_id={club_id}, "
                f"전역 권한: {global_roles}, 동아리 권한: {club_roles}, 합계: {all_roles}"
            )

            return all_roles

        except Exception as e:
            current_app.logger.exception(
                f"동아리 컨텍스트 권한 조회 중 오류 발생: user_id={user_id}, club_id={club_id}"
            )
            return set()

    def get_user_global_roles(self, user_id: int) -> Set[str]:
        """
        전역 권한 조회 (club_id가 NULL인 권한)

        Args:
            user_id: 사용자 ID

        Returns:
            전역 역할명 집합
        """
        try:
            memberships = (
                db.session.query(ClubMember, Role)
                .join(Role, ClubMember.role_id == Role.id)
                .filter(ClubMember.user_id == user_id, ClubMember.club_id.is_(None))
                .all()
            )

            return {role.role_name for _, role in memberships}

        except Exception as e:
            current_app.logger.exception(
                f"전역 권한 조회 중 오류 발생: user_id={user_id}"
            )
            return set()

    def has_role(
        self, user_id: int, role_name: str, club_id: Optional[int] = None
    ) -> bool:
        """
        사용자가 특정 역할을 가지고 있는지 확인

        Args:
            user_id: 사용자 ID
            role_name: 역할명
            club_id: 클럽 ID (None이면 전역 권한 확인)

        Returns:
            역할 보유 여부
        """
        if club_id is None:
            global_roles = self.get_user_global_roles(user_id)
            return role_name in global_roles
        else:
            club_roles = self.get_user_club_roles(user_id, club_id)
            return role_name in club_roles

    def has_any_role(
        self, user_id: int, role_names: Set[str], club_id: Optional[int] = None
    ) -> bool:
        """
        사용자가 여러 역할 중 하나라도 가지고 있는지 확인

        Args:
            user_id: 사용자 ID
            role_names: 역할명 집합
            club_id: 클럽 ID (None이면 전역 권한 확인)

        Returns:
            하나 이상의 역할 보유 여부
        """
        if club_id is None:
            user_roles = self.get_user_global_roles(user_id)
        else:
            user_roles = self.get_user_club_roles(user_id, club_id)

        return bool(user_roles.intersection(role_names))

    def clear_user_cache(self, user_id: int):
        """사용자 권한 캐시 삭제"""
        cache_key = f"user_roles_{user_id}"
        self._user_roles_cache.pop(cache_key, None)

    def clear_all_cache(self):
        """모든 권한 캐시 삭제"""
        self._user_roles_cache.clear()

    def get_permission_info(self, permission_key: str) -> Dict[str, Any]:
        """
        권한 정보 조회 (디버깅/관리용)

        Args:
            permission_key: 권한 키

        Returns:
            권한 정보 딕셔너리
        """
        policy = get_permission_policy(permission_key)
        if not policy:
            return {"error": f"권한 정책을 찾을 수 없습니다: {permission_key}"}

        return {
            "permission_key": permission_key,
            "description": policy.get("description", ""),
            "required_roles": policy["allowed_roles"],
            "role_hierarchy": ROLE_HIERARCHY,
        }


# 전역 인스턴스
permission_service = PermissionService()

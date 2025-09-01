from models import db, Role, User, Club, ClubMember


def create_role(name, description=None):
    """새로운 역할 생성"""
    try:
        # 중복 확인
        existing_role = Role.query.filter_by(role_name=name).first()
        if existing_role:
            raise ValueError(f"이미 존재하는 역할입니다: {name}")

        new_role = Role(role_name=name)
        db.session.add(new_role)
        db.session.commit()

        return {
            "id": new_role.id,
            "name": new_role.role_name,
            "description": new_role.description,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"역할 생성 중 오류 발생: {str(e)}")


def get_all_roles():
    """모든 역할 조회"""
    try:
        roles = Role.query.all()
        return [
            {"id": role.id, "name": role.role_name, "description": role.description}
            for role in roles
        ]

    except Exception as e:
        raise Exception(f"역할 조회 중 오류 발생: {str(e)}")


def get_role_by_id(role_id):
    """ID로 역할 조회"""
    try:
        role = Role.query.get(role_id)
        if not role:
            return None

        return {"id": role.id, "name": role.role_name, "description": role.description}

    except Exception as e:
        raise Exception(f"역할 조회 중 오류 발생: {str(e)}")


def assign_role_to_user_in_club(user_id, club_id, role_id):
    """사용자에게 특정 동아리에서 역할 부여"""
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다")

        club = Club.query.get(club_id)
        if not club:
            raise ValueError("동아리를 찾을 수 없습니다")

        role = Role.query.get(role_id)
        if not role:
            raise ValueError("역할을 찾을 수 없습니다")

        # 기존 멤버십 확인
        existing_membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if existing_membership:
            # 기존 멤버십 업데이트
            existing_membership.role_id = role_id
        else:
            # 새로운 멤버십 생성
            new_membership = ClubMember(
                user_id=user_id, club_id=club_id, role_id=role_id
            )
            db.session.add(new_membership)

        db.session.commit()

        return {
            "user_id": user.id,
            "user_name": user.name,
            "club_id": club.id,
            "club_name": club.name,
            "role_id": role.id,
            "role_name": role.role_name,
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"역할 부여 중 오류 발생: {str(e)}")


def get_user_role_in_club(user_id, club_id):
    """사용자의 특정 동아리에서의 역할 조회"""
    try:
        membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if not membership:
            return None

        return {
            "user_id": membership.user.id,
            "user_name": membership.user.name,
            "club_id": membership.club.id,
            "club_name": membership.club.name,
            "role_id": membership.role.id,
            "role_name": membership.role.role_name,
            "role_description": membership.role.description,
            "joined_at": membership.joined_at.isoformat()
            if membership.joined_at
            else None,
        }

    except Exception as e:
        raise Exception(f"사용자 역할 조회 중 오류 발생: {str(e)}")


def remove_user_role_from_club(user_id, club_id):
    """사용자의 특정 동아리에서의 역할 제거"""
    try:
        membership = ClubMember.query.filter_by(
            user_id=user_id, club_id=club_id
        ).first()

        if not membership:
            raise ValueError("해당 동아리의 멤버십을 찾을 수 없습니다")

        db.session.delete(membership)
        db.session.commit()

        return {
            "user_id": membership.user.id,
            "user_name": membership.user.name,
            "club_id": membership.club.id,
            "club_name": membership.club.name,
            "message": "역할이 제거되었습니다",
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"역할 제거 중 오류 발생: {str(e)}")


def get_users_by_role_in_club(club_id, role_id):
    """특정 동아리에서 특정 역할을 가진 사용자들 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("동아리를 찾을 수 없습니다")

        role = Role.query.get(role_id)
        if not role:
            raise ValueError("역할을 찾을 수 없습니다")

        memberships = ClubMember.query.filter_by(club_id=club_id, role_id=role_id).all()

        return [
            {
                "user_id": membership.user.id,
                "user_name": membership.user.name,
                "email": membership.user.email,
                "role_name": role.role_name,
                "joined_at": membership.joined_at.isoformat()
                if membership.joined_at
                else None,
            }
            for membership in memberships
        ]

    except Exception as e:
        raise Exception(f"역할별 사용자 조회 중 오류 발생: {str(e)}")


def get_all_club_members(club_id):
    """동아리의 모든 멤버 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("동아리를 찾을 수 없습니다")

        memberships = ClubMember.query.filter_by(club_id=club_id).all()

        return [
            {
                "user_id": membership.user.id,
                "user_name": membership.user.name,
                "email": membership.user.email,
                "role_id": membership.role.id,
                "role_name": membership.role.role_name,
                "joined_at": membership.joined_at.isoformat()
                if membership.joined_at
                else None,
            }
            for membership in memberships
        ]

    except Exception as e:
        raise Exception(f"동아리 멤버 조회 중 오류 발생: {str(e)}")


def check_current_user_permission(club_id, required_role=None):
    """현재 쿠키 세션을 통해 사용자의 동아리 권한 확인"""
    try:
        from services.session_service import get_current_user

        # 현재 세션에서 사용자 정보 조회
        user = get_current_user()
        if not user:
            return {
                "has_permission": False,
                "message": "로그인이 필요합니다",
                "user_id": None,
                "role": None,
            }

        # 사용자의 동아리 역할 조회
        membership = ClubMember.query.filter_by(
            user_id=user.id, club_id=club_id
        ).first()

        if not membership:
            return {
                "has_permission": False,
                "message": "해당 동아리의 멤버가 아닙니다",
                "user_id": user.id,
                "role": None,
            }

        user_role = membership.role.role_name

        # 특정 역할이 요구되는 경우
        if required_role:
            if user_role == required_role:
                return {
                    "has_permission": True,
                    "message": "권한이 확인되었습니다",
                    "user_id": user.id,
                    "role": user_role,
                }
            else:
                return {
                    "has_permission": False,
                    "message": f"필요한 권한: {required_role}, 현재 권한: {user_role}",
                    "user_id": user.id,
                    "role": user_role,
                }

        # 역할 확인만 하는 경우
        return {
            "has_permission": True,
            "message": "동아리 멤버입니다",
            "user_id": user.id,
            "role": user_role,
        }

    except Exception as e:
        raise Exception(f"권한 확인 중 오류 발생: {str(e)}")


def get_current_user_clubs():
    """현재 쿠키 세션을 통해 사용자가 속한 모든 동아리 조회"""
    try:
        from services.session_service import get_current_user

        # 현재 세션에서 사용자 정보 조회
        user = get_current_user()
        if not user:
            return []

        # 사용자의 모든 동아리 멤버십 조회
        memberships = ClubMember.query.filter_by(user_id=user.id).all()

        return [
            {
                "club_id": membership.club.id,
                "club_name": membership.club.name,
                "role_id": membership.role.id,
                "role_name": membership.role.role_name,
                "joined_at": membership.joined_at.isoformat()
                if membership.joined_at
                else None,
            }
            for membership in memberships
        ]

    except Exception as e:
        raise Exception(f"사용자 동아리 조회 중 오류 발생: {str(e)}")

import uuid
from datetime import datetime, timedelta
from flask import session
from models import db, UserSession
from utils.time_utils import get_kst_now, get_kst_now_naive


def create_session(user_id, expires_hours=24):
    """새로운 사용자 세션 생성 (쿠키에는 session_id만 저장)"""
    try:
        # 기존 활성 세션 비활성화
        deactivate_user_sessions(user_id)

        # 새 세션 생성
        session_id = str(uuid.uuid4())
        # MySQL은 naive datetime을 저장하므로 naive datetime 사용
        expires_at = get_kst_now_naive() + timedelta(hours=expires_hours)

        new_session = UserSession(
            session_id=session_id,
            user_id=user_id,
            expires_at=expires_at,
            is_active=True,
        )

        db.session.add(new_session)
        db.session.commit()

        # Flask 세션에는 session_id만 저장 (쿠키에 자동 저장됨)
        session["session_id"] = session_id

        result = {
            "session_id": session_id,
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
        }

        return result

    except Exception as e:
        db.session.rollback()
        raise Exception(f"세션 생성 중 오류 발생: {str(e)}")


def get_current_session():
    """현재 Flask 세션에서 세션 정보 조회 (쿠키에서 session_id만 읽기)"""
    try:
        session_id = session.get("session_id")

        if not session_id:
            return None

        # DB에서 세션 유효성 확인
        db_session = UserSession.query.filter_by(
            session_id=session_id, is_active=True
        ).first()

        if not db_session:
            clear_flask_session()
            return None

        # expires_at이 naive인 경우를 대비해 naive datetime으로 비교
        current_time = get_kst_now_naive()
        expires_at_naive = (
            db_session.expires_at.replace(tzinfo=None)
            if db_session.expires_at.tzinfo
            else db_session.expires_at
        )
        if current_time > expires_at_naive:
            deactivate_session(session_id)
            clear_flask_session()
            return None

        result = {
            "session_id": db_session.session_id,
            "user_id": db_session.user_id,
            "expires_at": db_session.expires_at.isoformat(),
        }

        return result

    except Exception as e:
        raise Exception(f"현재 세션 조회 중 오류 발생: {str(e)}")


def get_current_user():
    """현재 세션에서 사용자 정보 조회"""
    try:
        session_data = get_current_session()
        if not session_data:
            return None

        from models import User

        user = User.query.get(session_data["user_id"])

        return user

    except Exception as e:
        raise Exception(f"현재 사용자 조회 중 오류 발생: {str(e)}")


def clear_flask_session():
    """Flask 세션 클리어 (쿠키에서 session_id만 삭제)"""
    session.clear()


def validate_session(session_id):
    """세션 유효성 검증 (기존 방식 유지)"""
    try:
        session_obj = UserSession.query.filter_by(
            session_id=session_id, is_active=True
        ).first()

        if not session_obj:
            return None

        # 만료 시간 확인
        # expires_at이 naive인 경우를 대비해 naive datetime으로 비교
        current_time = get_kst_now_naive()
        expires_at_naive = (
            session_obj.expires_at.replace(tzinfo=None)
            if session_obj.expires_at.tzinfo
            else session_obj.expires_at
        )
        if current_time > expires_at_naive:
            deactivate_session(session_id)
            return None

        result = {
            "session_id": session_obj.session_id,
            "user_id": session_obj.user_id,
            "expires_at": session_obj.expires_at.isoformat(),
        }

        return result

    except Exception as e:
        raise Exception(f"세션 검증 중 오류 발생: {str(e)}")


def deactivate_session(session_id):
    """특정 세션 비활성화"""
    try:
        session_obj = UserSession.query.filter_by(session_id=session_id).first()

        if session_obj:
            session_obj.is_active = False
            db.session.commit()
        else:
            print("세션을 찾을 수 없습니다")

    except Exception as e:
        db.session.rollback()
        raise Exception(f"세션 비활성화 중 오류 발생: {str(e)}")


def deactivate_user_sessions(user_id):
    """사용자의 모든 세션 비활성화"""
    try:
        UserSession.query.filter_by(user_id=user_id, is_active=True).update(
            {"is_active": False}
        )
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(f"사용자 세션 비활성화 중 오류 발생: {str(e)}")


def cleanup_expired_sessions():
    """만료된 세션 정리"""
    try:
        # expires_at이 naive인 경우를 대비해 naive datetime으로 비교
        current_time = get_kst_now_naive()
        expired_sessions = UserSession.query.filter(
            UserSession.expires_at < current_time, UserSession.is_active == True
        ).all()

        for session_obj in expired_sessions:
            session_obj.is_active = False

        db.session.commit()

        return len(expired_sessions)

    except Exception as e:
        db.session.rollback()
        raise Exception(f"만료된 세션 정리 중 오류 발생: {str(e)}")


def debug_session_info():
    """현재 세션 상태 디버깅 정보 출력"""
    try:
        # Flask 세션 정보
        flask_session_id = session.get("session_id")

        # DB 세션 통계
        total_sessions = UserSession.query.count()
        active_sessions = UserSession.query.filter_by(is_active=True).count()
        # expires_at이 naive인 경우를 대비해 naive datetime으로 비교
        current_time = get_kst_now_naive()
        expired_sessions = UserSession.query.filter(
            UserSession.expires_at < current_time, UserSession.is_active == True
        ).count()

        # 현재 사용자 정보
        current_user = get_current_user()

        debug_info = {
            "flask_session_id": flask_session_id,
            "db_sessions": {
                "total": total_sessions,
                "active": active_sessions,
                "expired": expired_sessions,
            },
            "current_user": (
                {
                    "id": current_user.id if current_user else None,
                    "name": current_user.name if current_user else None,
                    "email": current_user.email if current_user else None,
                }
                if current_user
                else None
            ),
        }

        return debug_info

    except Exception as e:
        raise Exception(f"디버깅 정보 출력 중 오류 발생: {str(e)}")


def get_session_info():
    """현재 세션의 통합 정보 조회 (세션 + 사용자 + 권한 + 동아리)"""
    try:
        from flask import current_app

        current_app.logger.info("get_session_info: Starting session info retrieval")

        # 1. 현재 세션 정보 조회
        current_app.logger.info("get_session_info: Step 1 - Getting current session")
        session_data = get_current_session()
        current_app.logger.info(f"get_session_info: Session data: {session_data}")
        if not session_data:
            current_app.logger.warning("get_session_info: No session data found")
            return None

        # 2. 사용자 정보 조회
        current_app.logger.info("get_session_info: Step 2 - Getting current user")
        user = get_current_user()
        current_app.logger.info(
            f"get_session_info: User data: {user.id if user else None}"
        )
        if not user:
            current_app.logger.warning("get_session_info: No user found")
            return None

        # 3. 사용자의 동아리 멤버십 정보 조회
        current_app.logger.info("get_session_info: Step 3 - Getting club memberships")
        from models.club_member import ClubMember

        current_app.logger.info(
            f"get_session_info: Querying memberships for user_id: {user.id}"
        )
        try:
            memberships = ClubMember.query.filter_by(user_id=user.id).all()
            current_app.logger.info(
                f"get_session_info: Found {len(memberships)} memberships"
            )
        except Exception as e:
            current_app.logger.error(
                f"get_session_info: Error querying memberships: {str(e)}"
            )
            raise

        clubs_info = []
        for membership in memberships:
            try:
                current_app.logger.info(
                    f"get_session_info: Processing membership: {membership.id}, club_id: {membership.club_id}"
                )

                # club_id가 None인 경우 (전역 역할) 처리
                if membership.club_id is None:
                    club_info = {
                        "club_id": None,
                        "club_name": "전역 역할",
                        "role_id": membership.role.id,
                        "role_name": membership.role.role_name,
                        "joined_at": (
                            membership.joined_at.isoformat()
                            if membership.joined_at
                            else None
                        ),
                    }
                else:
                    club_info = {
                        "club_id": membership.club.id,
                        "club_name": membership.club.name,
                        "role_id": membership.role.id,
                        "role_name": membership.role.role_name,
                        "joined_at": (
                            membership.joined_at.isoformat()
                            if membership.joined_at
                            else None
                        ),
                    }
                clubs_info.append(club_info)
                current_app.logger.info(
                    f"get_session_info: Added club info: {club_info}"
                )

            except Exception as e:
                current_app.logger.error(
                    f"get_session_info: Error processing membership {membership.id}: {str(e)}"
                )
                raise

        # 4. 통합 정보 구성
        current_app.logger.info("get_session_info: Step 4 - Creating session info")
        session_info = {
            "session": {
                "session_id": session_data["session_id"],
                "user_id": session_data["user_id"],
                "expires_at": session_data["expires_at"],
            },
            "user": {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "student_id": user.student_id,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "department_id": user.department_id,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            },
            "clubs": clubs_info,
            "total_clubs": len(clubs_info),
        }

        current_app.logger.info("get_session_info: Successfully created session info")
        return session_info

    except Exception as e:
        from flask import current_app

        current_app.logger.exception("get_session_info: Exception occurred")
        current_app.logger.error(f"get_session_info: Exception details: {str(e)}")
        current_app.logger.error(f"get_session_info: Exception type: {type(e)}")
        raise Exception(f"세션 통합 정보 조회 중 오류 발생: {str(e)}")

import uuid
from datetime import datetime, timedelta
from flask import session
from models import db, UserSession


def create_session(user_id, expires_hours=24):
    """새로운 사용자 세션 생성 (쿠키에는 session_id만 저장)"""
    try:
        print(f"🔍 [DEBUG] 세션 생성 시작 - user_id: {user_id}")
        
        # 기존 활성 세션 비활성화
        deactivate_user_sessions(user_id)
        print(f"🔍 [DEBUG] 기존 세션 비활성화 완료")
        
        # 새 세션 생성
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
        
        print(f"🔍 [DEBUG] 새 세션 ID 생성: {session_id}")
        print(f"🔍 [DEBUG] 만료 시간: {expires_at}")
        
        new_session = UserSession(
            session_id=session_id,
            user_id=user_id,
            expires_at=expires_at,
            is_active=True
        )
        
        print(f"🔍 [DEBUG] DB에 세션 정보 저장 중...")
        db.session.add(new_session)
        db.session.commit()
        print(f"🔍 [DEBUG] DB 세션 저장 완료!")
        
        # Flask 세션에는 session_id만 저장 (쿠키에 자동 저장됨)
        session['session_id'] = session_id
        print(f"🔍 [DEBUG] Flask 세션에 session_id 저장: {session_id}")
        print(f"🔍 [DEBUG] 쿠키에 자동으로 session_id가 저장됩니다")
        
        result = {
            "session_id": session_id,
            "user_id": user_id,
            "expires_at": expires_at.isoformat()
        }
        
        print(f"🔍 [DEBUG] 세션 생성 완료: {result}")
        return result
        
    except Exception as e:
        print(f"❌ [DEBUG] 세션 생성 실패: {str(e)}")
        db.session.rollback()
        raise Exception(f"세션 생성 중 오류 발생: {str(e)}")


def get_current_session():
    """현재 Flask 세션에서 세션 정보 조회 (쿠키에서 session_id만 읽기)"""
    try:
        session_id = session.get('session_id')
        print(f"🔍 [DEBUG] 쿠키에서 session_id 읽기: {session_id}")
        
        if not session_id:
            print(f"🔍 [DEBUG] 쿠키에 session_id가 없습니다")
            return None
            
        # DB에서 세션 유효성 확인
        print(f"🔍 [DEBUG] DB에서 세션 정보 조회 중...")
        db_session = UserSession.query.filter_by(
            session_id=session_id,
            is_active=True
        ).first()
        
        if not db_session:
            print(f"🔍 [DEBUG] DB에서 세션을 찾을 수 없습니다")
            clear_flask_session()
            return None
        
        if datetime.utcnow() > db_session.expires_at:
            print(f"🔍 [DEBUG] 세션이 만료되었습니다")
            deactivate_session(session_id)
            clear_flask_session()
            return None
        
        result = {
            "session_id": db_session.session_id,
            "user_id": db_session.user_id,
            "expires_at": db_session.expires_at.isoformat()
        }
        
        print(f"🔍 [DEBUG] 세션 정보 조회 완료: {result}")
        return result
        
    except Exception as e:
        print(f"❌ [DEBUG] 세션 조회 실패: {str(e)}")
        raise Exception(f"현재 세션 조회 중 오류 발생: {str(e)}")


def get_current_user():
    """현재 세션에서 사용자 정보 조회"""
    try:
        print(f"🔍 [DEBUG] 현재 사용자 정보 조회 시작")
        session_data = get_current_session()
        if not session_data:
            print(f"🔍 [DEBUG] 세션 데이터가 없습니다")
            return None
            
        from models import User
        user = User.query.get(session_data['user_id'])
        
        if user:
            print(f"🔍 [DEBUG] 사용자 정보 조회 완료: {user.name} ({user.email})")
        else:
            print(f"🔍 [DEBUG] 사용자를 찾을 수 없습니다")
            
        return user
        
    except Exception as e:
        print(f"❌ [DEBUG] 사용자 조회 실패: {str(e)}")
        raise Exception(f"현재 사용자 조회 중 오류 발생: {str(e)}")


def clear_flask_session():
    """Flask 세션 클리어 (쿠키에서 session_id만 삭제)"""
    print(f"🔍 [DEBUG] Flask 세션 클리어 (쿠키 삭제)")
    session.clear()


def validate_session(session_id):
    """세션 유효성 검증 (기존 방식 유지)"""
    try:
        print(f"🔍 [DEBUG] 세션 유효성 검증: {session_id}")
        session_obj = UserSession.query.filter_by(
            session_id=session_id,
            is_active=True
        ).first()
        
        if not session_obj:
            print(f"🔍 [DEBUG] 세션을 찾을 수 없습니다")
            return None
        
        # 만료 시간 확인
        if datetime.utcnow() > session_obj.expires_at:
            print(f"🔍 [DEBUG] 세션이 만료되었습니다")
            deactivate_session(session_id)
            return None
        
        result = {
            "session_id": session_obj.session_id,
            "user_id": session_obj.user_id,
            "expires_at": session_obj.expires_at.isoformat()
        }
        
        print(f"🔍 [DEBUG] 세션 유효성 검증 완료: {result}")
        return result
        
    except Exception as e:
        print(f"❌ [DEBUG] 세션 검증 실패: {str(e)}")
        raise Exception(f"세션 검증 중 오류 발생: {str(e)}")


def deactivate_session(session_id):
    """특정 세션 비활성화"""
    try:
        print(f"🔍 [DEBUG] 세션 비활성화: {session_id}")
        session_obj = UserSession.query.filter_by(session_id=session_id).first()
        if session_obj:
            session_obj.is_active = False
            db.session.commit()
            print(f"🔍 [DEBUG] 세션 비활성화 완료")
        else:
            print(f"🔍 [DEBUG] 비활성화할 세션을 찾을 수 없습니다")
            
    except Exception as e:
        print(f"❌ [DEBUG] 세션 비활성화 실패: {str(e)}")
        db.session.rollback()
        raise Exception(f"세션 비활성화 중 오류 발생: {str(e)}")


def deactivate_user_sessions(user_id):
    """사용자의 모든 세션 비활성화"""
    try:
        print(f"🔍 [DEBUG] 사용자 세션 비활성화: user_id {user_id}")
        UserSession.query.filter_by(
            user_id=user_id,
            is_active=True
        ).update({"is_active": False})
        db.session.commit()
        print(f"🔍 [DEBUG] 사용자 세션 비활성화 완료")
        
    except Exception as e:
        print(f"❌ [DEBUG] 사용자 세션 비활성화 실패: {str(e)}")
        db.session.rollback()
        raise Exception(f"사용자 세션 비활성화 중 오류 발생: {str(e)}")





def cleanup_expired_sessions():
    """만료된 세션 정리"""
    try:
        print(f"🔍 [DEBUG] 만료된 세션 정리 시작")
        expired_sessions = UserSession.query.filter(
            UserSession.expires_at < datetime.utcnow(),
            UserSession.is_active == True
        ).all()
        
        print(f"🔍 [DEBUG] 만료된 세션 수: {len(expired_sessions)}")
        
        for session_obj in expired_sessions:
            session_obj.is_active = False
        
        db.session.commit()
        print(f"🔍 [DEBUG] 만료된 세션 정리 완료")
        
        return len(expired_sessions)
        
    except Exception as e:
        print(f"❌ [DEBUG] 세션 정리 실패: {str(e)}")
        db.session.rollback()
        raise Exception(f"만료된 세션 정리 중 오류 발생: {str(e)}")


def debug_session_info():
    """현재 세션 상태 디버깅 정보 출력"""
    try:
        print(f"\n🔍 [DEBUG] === 세션 상태 디버깅 ===")
        
        # Flask 세션 정보
        flask_session_id = session.get('session_id')
        print(f"🔍 [DEBUG] Flask 세션 ID: {flask_session_id}")
        
        # DB 세션 통계
        total_sessions = UserSession.query.count()
        active_sessions = UserSession.query.filter_by(is_active=True).count()
        expired_sessions = UserSession.query.filter(
            UserSession.expires_at < datetime.utcnow(),
            UserSession.is_active == True
        ).count()
        
        print(f"🔍 [DEBUG] DB 세션 통계:")
        print(f"  - 전체 세션: {total_sessions}")
        print(f"  - 활성 세션: {active_sessions}")
        print(f"  - 만료된 세션: {expired_sessions}")
        
        # 현재 사용자 정보
        current_user = get_current_user()
        if current_user:
            print(f"🔍 [DEBUG] 현재 사용자: {current_user.name} ({current_user.email})")
        else:
            print(f"🔍 [DEBUG] 현재 사용자: 로그인되지 않음")
            
        print(f"🔍 [DEBUG] === 디버깅 완료 ===\n")
        
    except Exception as e:
        print(f"❌ [DEBUG] 디버깅 정보 출력 실패: {str(e)}")


def get_session_info():
    """현재 세션의 통합 정보 조회 (세션 + 사용자 + 권한 + 동아리)"""
    try:
        print(f"🔍 [DEBUG] 세션 통합 정보 조회 시작")
        
        # 1. 현재 세션 정보 조회
        session_data = get_current_session()
        if not session_data:
            print(f"🔍 [DEBUG] 유효한 세션이 없습니다")
            return None
        
        # 2. 사용자 정보 조회
        user = get_current_user()
        if not user:
            print(f"🔍 [DEBUG] 사용자 정보를 찾을 수 없습니다")
            return None
        
        # 3. 사용자의 동아리 멤버십 정보 조회
        from models.club_member import ClubMember
        memberships = ClubMember.query.filter_by(user_id=user.id).all()
        
        clubs_info = []
        for membership in memberships:
            club_info = {
                "club_id": membership.club.id,
                "club_name": membership.club.name,
                "role_id": membership.role.id,
                "role_name": membership.role.role_name,
                "joined_at": membership.joined_at.isoformat() if membership.joined_at else None
            }
            clubs_info.append(club_info)
        
        # 4. 통합 정보 구성
        session_info = {
            "session": {
                "session_id": session_data["session_id"],
                "user_id": session_data["user_id"],
                "expires_at": session_data["expires_at"]
            },
            "user": {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None
            },
            "clubs": clubs_info,
            "total_clubs": len(clubs_info)
        }
        
        print(f"🔍 [DEBUG] 세션 통합 정보 조회 완료")
        print(f"🔍 [DEBUG] 사용자: {user.name}, 동아리 수: {len(clubs_info)}")
        
        return session_info
        
    except Exception as e:
        print(f"❌ [DEBUG] 세션 통합 정보 조회 실패: {str(e)}")
        raise Exception(f"세션 통합 정보 조회 중 오류 발생: {str(e)}")

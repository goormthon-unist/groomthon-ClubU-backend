import re
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def validate_email(email):
    """이메일 형식 검증"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password(password):
    """비밀번호 강도 검증"""
    if len(password) < 6:
        return False, "비밀번호는 최소 6자 이상이어야 합니다."

    return True, "비밀번호가 유효합니다."


def validate_username(username):
    """사용자명 형식 검증"""
    if len(username) < 3:
        return False, "사용자명은 최소 3자 이상이어야 합니다."

    if len(username) > 20:
        return False, "사용자명은 최대 20자까지 가능합니다."

    # 영문, 숫자, 언더스코어만 허용
    pattern = r"^[a-zA-Z0-9_]+$"
    if not re.match(pattern, username):
        return False, "사용자명은 영문, 숫자, 언더스코어(_)만 사용 가능합니다."

    return True, "사용자명이 유효합니다."


def create_user(user_data):
    """새 사용자 생성 (간단한 회원가입용)"""
    try:
        # 이메일 중복 확인
        existing_email = User.query.filter_by(email=user_data["email"]).first()
        if existing_email:
            raise ValueError("이미 등록된 이메일입니다.")

        # 새 사용자 생성 (필수 필드만)
        new_user = User(
            name=user_data["username"],  # username을 name으로 사용
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
            student_id="00000000",  # 임시 학번
            department_id=1,  # 임시 학과 ID
            phone_number="010-0000-0000",  # 임시 전화번호
        )

        # 데이터베이스에 저장
        db.session.add(new_user)
        db.session.commit()

        return {
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "created_at": (
                new_user.created_at.isoformat() if new_user.created_at else None
            ),
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"사용자 생성 중 오류 발생: {str(e)}")


def authenticate_user(email, password):
    """사용자 인증"""
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")

        if not check_password_hash(user.password, password):
            raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")

        return {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    except Exception as e:
        raise Exception(f"사용자 인증 중 오류 발생: {str(e)}")


def get_all_users():
    """모든 사용자 정보 조회"""
    try:
        users = User.query.all()

        user_list = []
        for user in users:
            user_info = {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "student_id": user.student_id,
                "department_id": user.department_id,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "email_verified_at": (
                    user.email_verified_at.isoformat()
                    if user.email_verified_at
                    else None
                ),
                "created_at": (
                    user.created_at.isoformat() if user.created_at else None
                ),
                "updated_at": (
                    user.updated_at.isoformat() if user.updated_at else None
                ),
            }
            user_list.append(user_info)

        return user_list

    except Exception as e:
        raise Exception(f"사용자 목록 조회 중 오류 발생: {str(e)}")

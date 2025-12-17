import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role, ClubMember


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
    # 실제 사용자 이름 용도로 사용되므로, 최소 2자 이상 허용
    if len(username) < 2:
        return False, "이름은 최소 2자 이상이어야 합니다."

    if len(username) > 20:
        return False, "이름은 최대 20자까지 가능합니다."

    # 영문/한글만 허용 (실제 사용자 이름용)
    pattern = r"^[a-zA-Z가-힣]+$"
    if not re.match(pattern, username):
        return False, "이름은 영문 또는 한글만 사용 가능합니다."

    return True, "이름이 유효합니다."


def validate_student_id(student_id):
    """학번 형식 검증"""
    if len(student_id) != 8:
        return False, "학번은 8자리여야 합니다."

    if not student_id.isdigit():
        return False, "학번은 숫자만 입력 가능합니다."

    return True, "학번이 유효합니다."


def validate_phone_number(phone_number):
    """전화번호 형식 검증"""
    # 010-1234-5678 형식 또는 01012345678 형식 허용
    pattern = r"^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$"
    if not re.match(pattern, phone_number):
        return (
            False,
            "전화번호 형식이 올바르지 않습니다. (예: 010-1234-5678 또는 01012345678)",
        )

    return True, "전화번호가 유효합니다."


def create_user(user_data):
    """새 사용자 생성 (간단한 회원가입용)"""
    try:
        # 이메일 중복 확인
        existing_email = User.query.filter_by(email=user_data["email"]).first()
        if existing_email:
            raise ValueError("이미 등록된 이메일입니다.")

        # 학번 중복 확인
        existing_student_id = User.query.filter_by(
            student_id=user_data["student_id"]
        ).first()
        if existing_student_id:
            raise ValueError("이미 등록된 학번입니다.")

        # 새 사용자 생성 (필수 필드만)
        new_user = User(
            name=user_data["username"],  # username을 name으로 사용
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
            student_id=user_data["student_id"],  # 실제 학번
            department_id=user_data["department_id"],  # 사용자가 선택한 학과
            phone_number=user_data["phone_number"],  # 실제 전화번호
            gender=user_data.get("gender"),  # 성별 (선택사항)
        )

        # 데이터베이스에 저장
        db.session.add(new_user)
        db.session.flush()  # ID 생성

        # 기본 STUDENT 역할 부여 (전역 역할)
        student_role = Role.query.filter_by(role_name="STUDENT").first()
        if not student_role:
            raise Exception(
                "STUDENT 역할이 존재하지 않습니다. 시스템 관리자에게 문의하세요."
            )

        club_member = ClubMember(
            user_id=new_user.id,
            club_id=None,  # 전역 역할 (NULL)
            role_id=student_role.id,
            generation=1,  # 기본값
            joined_at=datetime.utcnow(),
        )
        db.session.add(club_member)
        db.session.commit()

        return {
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "student_id": new_user.student_id,
            "phone_number": new_user.phone_number,
            "gender": new_user.gender,
            "role": "STUDENT",  # 부여된 역할 정보 추가
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

    except ValueError:
        # ValueError는 그대로 전달 (401 처리용)
        raise
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

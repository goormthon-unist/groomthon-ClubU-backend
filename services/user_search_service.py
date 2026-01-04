"""
사용자 검색 서비스
학번과 이름으로 사용자를 검색하고 검증하는 기능
"""

from typing import Dict, Any
from models import User


def find_user_by_student_id_and_name(student_id: str, name: str) -> Dict[str, Any]:
    """
    학번과 이름으로 사용자 검색 및 검증

    Args:
        student_id: 학번
        name: 이름

    Returns:
        Dict with user information

    Raises:
        ValueError: 사용자를 찾을 수 없거나 이름이 일치하지 않는 경우
    """
    try:
        # 학번으로 사용자 검색
        user = User.query.filter_by(student_id=student_id).first()

        # 보안: 학번 존재 여부와 이름 일치 여부를 구분하지 않음
        # 학번이 없거나 이름이 일치하지 않으면 동일한 오류 메시지 반환
        if not user or user.name != name:
            raise ValueError("학번과 이름이 일치하지 않습니다.")

        return {
            "success": True,
            "user_id": user.id,
            "name": user.name,
            "student_id": user.student_id,
            "email": user.email,
            "department": (
                {
                    "id": user.department.id,
                    "name": f"{user.department.college} {user.department.major}",
                }
                if user.department
                else None
            ),
        }

    except ValueError:
        # ValueError는 그대로 전달
        raise
    except Exception as e:
        raise Exception(f"사용자 검색 중 오류 발생: {str(e)}")

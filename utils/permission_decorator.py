"""
권한 검사 데코레이터
컨트롤러에서 @require_permission("permission_key") 형태로 사용
"""

from functools import wraps
from flask import request, jsonify
from services.permission_service import permission_service
from config.permission_policy import CLUB_SCOPED_PERMISSIONS


def require_permission(permission_key: str, club_id_param: str = None):
    """
    권한 검사 데코레이터

    사용법:
        @require_permission("clubs.update")
        def put(self, club_id):
            # 권한 검사 통과 후 실행되는 코드
            pass

        @require_permission("clubs.members", club_id_param="club_id")
        def get(self, club_id):
            # club_id 파라미터를 동아리 컨텍스트로 사용
            pass

    Args:
        permission_key: 권한 키 (config/permission_policy.py에 정의된 키)
        club_id_param: 동아리 ID 파라미터명 (kwargs에서 추출하여 컨텍스트로 사용)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # OPTIONS 요청 (CORS preflight)은 권한 검사 건너뛰기
            if request.method == "OPTIONS":
                return f(*args, **kwargs)

            # 동아리 컨텍스트 추출
            club_id = None
            # 1) kwargs 우선
            if club_id_param and club_id_param in kwargs:
                try:
                    club_id = int(kwargs[club_id_param])
                except (ValueError, TypeError):
                    return {
                        "status": "error",
                        "message": f"유효하지 않은 {club_id_param} 파라미터입니다",
                        "code": "400-00",
                    }, 400
            # 2) kwargs에 없고 positional로 전달된 경우(super().get(club_id) 패턴)
            elif club_id_param and club_id is None and len(args) >= 2:
                try:
                    club_id = int(args[1])
                except (ValueError, TypeError):
                    return {
                        "status": "error",
                        "message": f"유효하지 않은 {club_id_param} 파라미터입니다",
                        "code": "400-00",
                    }, 400
            # club 스코프 권한인데 club_id가 없는 경우
            if club_id is None and permission_key in CLUB_SCOPED_PERMISSIONS:
                return {
                    "status": "error",
                    "message": "club_id가 필요합니다",
                    "code": "400-00",
                }, 400

            # 권한 검사 실행
            result = permission_service.check_permission(
                permission_key, club_id=club_id
            )

            if not result["has_permission"]:
                # 권한 부족 시 HTTP 상태 코드 결정
                if not result["user_id"]:
                    # 로그인 필요
                    return {
                        "status": "error",
                        "message": result["message"],
                        "code": "401-01",
                    }, 401
                else:
                    # 권한 부족
                    return {
                        "status": "error",
                        "message": result["message"],
                        "code": "403-01",
                    }, 403

            # 권한 검사 통과 - 원래 함수 실행
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_any_permission(*permission_keys: str):
    """
    여러 권한 중 하나라도 있으면 통과하는 데코레이터

    사용법:
        @require_any_permission("clubs.update", "clubs.delete")
        def put(self, club_id):
            pass

    Args:
        *permission_keys: 권한 키들 (하나라도 통과하면 OK)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # OPTIONS 요청 (CORS preflight)은 권한 검사 건너뛰기
            if request.method == "OPTIONS":
                return f(*args, **kwargs)

            # 모든 권한 검사
            results = []
            for permission_key in permission_keys:
                result = permission_service.check_permission(permission_key)
                results.append(result)
                if result["has_permission"]:
                    # 하나라도 통과하면 OK
                    return f(*args, **kwargs)

            # 모든 권한 검사 실패
            if not any(r["user_id"] for r in results):
                # 로그인 필요
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401
            else:
                # 권한 부족
                required_roles = set()
                for result in results:
                    required_roles.update(result["required_roles"])
                return {
                    "status": "error",
                    "message": f"권한이 부족합니다. 필요 권한: {', '.join(required_roles)}",
                    "code": "403-01",
                }, 403

        return decorated_function

    return decorator


def require_all_permissions(*permission_keys: str):
    """
    모든 권한이 있어야 통과하는 데코레이터

    사용법:
        @require_all_permissions("clubs.update", "clubs.members")
        def put(self, club_id):
            pass

    Args:
        *permission_keys: 권한 키들 (모두 있어야 통과)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # OPTIONS 요청 (CORS preflight)은 권한 검사 건너뛰기
            if request.method == "OPTIONS":
                return f(*args, **kwargs)

            # 모든 권한 검사
            results = []
            for permission_key in permission_keys:
                result = permission_service.check_permission(permission_key)
                results.append(result)
                if not result["has_permission"]:
                    # 하나라도 실패하면 중단
                    if not result["user_id"]:
                        return {
                            "status": "error",
                            "message": result["message"],
                            "code": "401-01",
                        }, 401
                    else:
                        return {
                            "status": "error",
                            "message": result["message"],
                            "code": "403-01",
                        }, 403

            # 모든 권한 검사 통과
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def optional_permission(permission_key: str):
    """
    권한이 있으면 추가 정보를 제공하는 데코레이터
    권한이 없어도 실행되지만, request 객체에 권한 정보를 추가

    사용법:
        @optional_permission("clubs.update")
        def get(self, club_id):
            if hasattr(request, 'user_has_permission'):
                # 권한이 있는 경우의 추가 로직
                pass
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 권한 검사 실행
            result = permission_service.check_permission(permission_key)

            # request 객체에 권한 정보 추가
            request.user_has_permission = result["has_permission"]
            request.user_permission_info = result

            # 권한 여부와 관계없이 함수 실행
            return f(*args, **kwargs)

        return decorated_function

    return decorator

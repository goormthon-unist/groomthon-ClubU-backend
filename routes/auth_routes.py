from flask_restx import Namespace
from controllers.auth_controller import (
    RegisterController,
    LoginController,
    LogoutController,
    SessionDebugController,
    SessionInfoController,
)

# 네임스페이스 등록
auth_ns = Namespace("auth", description="인증 관리 API")


# API 엔드포인트 등록
@auth_ns.route("/register")
class RegisterResource(RegisterController):
    """회원가입 리소스"""

    pass


@auth_ns.route("/login")
class LoginResource(LoginController):
    """로그인 리소스"""

    pass


@auth_ns.route("/logout")
class LogoutResource(LogoutController):
    """로그아웃 리소스"""

    pass


@auth_ns.route("/debug/session")
class SessionDebugResource(SessionDebugController):
    """세션 디버깅 리소스"""

    pass


@auth_ns.route("/session-info")
class SessionInfoResource(SessionInfoController):
    """세션 통합 정보 조회 리소스"""

    pass

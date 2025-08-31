from flask_restx import Namespace
from controllers.auth_controller import (
    RegisterController,
    LoginController,
    UserListController,
)

# 네임스페이스 등록
auth_ns = Namespace("auth", description="인증 관련 API")


# API 엔드포인트 등록
@auth_ns.route("/register")
class RegisterResource(RegisterController):
    """회원가입 리소스"""

    pass


@auth_ns.route("/login")
class LoginResource(LoginController):
    """로그인 리소스"""

    pass


@auth_ns.route("/users")
class UsersResource(UserListController):
    """사용자 목록 조회 리소스 (테스트용)"""

    pass

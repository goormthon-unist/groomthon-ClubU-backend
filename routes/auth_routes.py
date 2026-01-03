from flask_restx import Namespace, fields
from controllers.auth_controller import (
    RegisterController,
    LoginController,
    LogoutController,
    SessionDebugController,
    SessionInfoController,
    UserListController,
)

# 네임스페이스 등록
auth_ns = Namespace("auth", description="인증 관리 API")

# Request Body 모델 정의
register_model = auth_ns.model(
    "Register",
    {
        "username": fields.String(required=True, description="사용자명"),
        "email": fields.String(required=True, description="이메일"),
        "password": fields.String(required=True, description="비밀번호"),
        "student_id": fields.String(required=True, description="학번 (8자리)"),
        "phone_number": fields.String(
            required=True, description="전화번호 (010-XXXX-XXXX)"
        ),
        "department_id": fields.Integer(required=True, description="학과 ID"),
        "gender": fields.String(
            required=True, description="성별", enum=["MALE", "FEMALE", "OTHER"]
        ),
    },
)

login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="이메일"),
        "password": fields.String(required=True, description="비밀번호"),
        "channel": fields.String(
            required=True, description="로그인 채널", enum=["WEB", "APP"]
        ),
        "device_id": fields.String(
            required=False,
            description="APP 로그인 시 필수, UUID 형식(최대 64자)",
        ),
    },
)


# API 엔드포인트 등록
@auth_ns.route("/register")
class RegisterResource(RegisterController):
    """회원가입 리소스"""

    @auth_ns.doc("register")
    @auth_ns.expect(register_model)
    @auth_ns.response(201, "회원가입 성공")
    @auth_ns.response(400, "잘못된 요청")
    @auth_ns.response(500, "서버 내부 오류")
    def post(self):
        """회원가입"""
        return super().post()


@auth_ns.route("/login")
class LoginResource(LoginController):
    """로그인 리소스"""

    @auth_ns.doc("login")
    @auth_ns.expect(login_model)
    @auth_ns.response(200, "로그인 성공")
    @auth_ns.response(400, "잘못된 요청")
    @auth_ns.response(401, "인증 실패")
    @auth_ns.response(500, "서버 내부 오류")
    def post(self):
        """로그인"""
        return super().post()


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


@auth_ns.route("/users")
class UserListResource(UserListController):
    """모든 사용자 목록 조회 리소스"""

    pass

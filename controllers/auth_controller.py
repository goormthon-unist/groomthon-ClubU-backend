from flask_restx import Resource, abort, reqparse
from werkzeug.exceptions import HTTPException, BadRequest
from flask import request, current_app
from services.auth_service import (
    create_user,
    authenticate_user,
    validate_username,
    validate_email,
    validate_password,
)
from services.session_service import (
    create_session,
    deactivate_session,
    clear_flask_session,
    debug_session_info,
    get_current_user,
)


class RegisterController(Resource):
    """회원가입 컨트롤러"""

    def post(self):
        """회원가입 API"""
        try:
            # 1) JSON 파싱: 잘못된 JSON이면 BadRequest 유발
            try:
                data = request.get_json(force=False, silent=False)
            except BadRequest:
                abort(400, "400-00: invalid JSON body")

            if not isinstance(data, dict):
                abort(400, "400-00: JSON object is required")

            # 2) 필드 추출/검증
            username = (data.get("username") or "").strip()
            email = (data.get("email") or "").strip()
            password = data.get("password")

            if not username:
                abort(400, "400-01: username is required")
            if not email:
                abort(400, "400-02: email is required")
            if not password:
                abort(400, "400-03: password is required")

            # 3) 상세 형식 검증
            is_valid_username, username_message = validate_username(username)
            if not is_valid_username:
                abort(400, f"400-04: {username_message}")

            if not validate_email(email):
                abort(400, "400-05: 유효하지 않은 이메일 형식입니다.")

            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                abort(400, f"400-06: {password_message}")

            # 4) 사용자 생성
            user_data = create_user(
                {
                    "username": username,
                    "email": email,
                    "password": password,
                }
            )

            return {
                "status": "success",
                "message": "회원가입이 완료되었습니다.",
                "data": user_data,
            }, 201

        except HTTPException as he:
            # 400/401/409 등은 그대로 내보냄 (500으로 덮어쓰지 않음)
            raise he
        except ValueError as e:
            abort(400, f"400-07: {str(e)}")
        except Exception as e:
            current_app.logger.exception("auth.register failed")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class LoginController(Resource):
    """로그인 컨트롤러"""

    def post(self):
        """로그인 API"""
        try:
            # 1) JSON 파싱: 잘못된 JSON이면 BadRequest 유발
            try:
                data = request.get_json(force=False, silent=False)
            except BadRequest:
                abort(400, "400-00: invalid JSON body")

            if not isinstance(data, dict):
                abort(400, "400-00: JSON object is required")

            # 2) 필드 추출/검증
            email = (data.get("email") or "").strip()
            password = data.get("password")

            if not email:
                abort(400, "400-01: email is required")
            if not password:
                abort(400, "400-02: password is required")

            # 3) 사용자 인증
            user_data = authenticate_user(email, password)

            # 4) 세션 생성
            session_data = create_session(user_data["user_id"])

            response_data = {
                "status": "success",
                "message": "로그인이 완료되었습니다.",
                "data": {"user": user_data, "session": session_data},
            }

            return response_data, 200

        except HTTPException as he:
            # 400/401/409 등은 그대로 내보냄 (500으로 덮어쓰지 않음)
            raise he
        except ValueError as e:
            abort(401, f"401-01: {str(e)}")
        except Exception as e:
            current_app.logger.exception("auth.login failed")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class LogoutController(Resource):
    """로그아웃 컨트롤러"""

    def post(self):
        """로그아웃 API"""
        try:
            # 현재 세션 정보 조회
            current_session = get_current_session()

            if current_session:
                # 세션 비활성화
                deactivate_session(current_session["session_id"])

            # Flask 세션 클리어
            clear_flask_session()

            response_data = {
                "status": "success",
                "message": "로그아웃이 완료되었습니다.",
            }

            return response_data, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class SessionDebugController(Resource):
    """세션 디버깅 컨트롤러"""

    def get(self):
        """현재 세션 상태 디버깅 정보를 반환합니다"""
        try:
            debug_info = debug_session_info()

            return {"status": "success", "debug_info": debug_info}, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class SessionInfoController(Resource):
    """세션 통합 정보 조회 컨트롤러"""

    def get(self):
        """현재 세션의 통합 정보 조회 API (세션 + 사용자 + 권한 + 동아리)"""
        try:
            from services.session_service import get_session_info

            # 세션 통합 정보 조회
            session_info = get_session_info()

            if not session_info:
                abort(401, "401-01: 로그인이 필요합니다")

            response_data = {
                "status": "success",
                "message": "세션 통합 정보를 조회했습니다.",
                "data": session_info,
            }

            return response_data, 200

        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

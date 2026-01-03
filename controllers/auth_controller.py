from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest
from flask import request, current_app
import uuid
from services.auth_service import (
    create_user,
    authenticate_user,
    validate_username,
    validate_email,
    validate_password,
    validate_student_id,
    validate_phone_number,
    get_all_users,
)
from services.session_service import (
    create_session,
    deactivate_session,
    clear_flask_session,
    debug_session_info,
    get_current_user,
    get_current_session,
)


class RegisterController(Resource):
    """회원가입 컨트롤러"""

    def post(self):
        """회원가입 API"""
        try:
            # 1) JSON 파싱: 잘못된 JSON이면 BadRequest 유발
            try:
                data = request.get_json(force=False, silent=False)
                current_app.logger.info(f"Register request data: {data}")
            except BadRequest as e:
                current_app.logger.error(f"JSON parsing error: {str(e)}")
                return {
                    "status": "error",
                    "message": "유효하지 않은 JSON 형식입니다",
                    "code": "400-00",
                }, 400

            if not isinstance(data, dict):
                current_app.logger.error("Request data is not a dict")
                return {
                    "status": "error",
                    "message": "JSON 객체가 필요합니다",
                    "code": "400-00",
                }, 400

            # 2) 필드 추출/검증
            username = (data.get("username") or "").strip()
            email = (data.get("email") or "").strip()
            password = data.get("password")
            student_id = (data.get("student_id") or "").strip()
            phone_number = (data.get("phone_number") or "").strip()
            department_id = data.get("department_id")
            gender = data.get("gender")

            current_app.logger.info(
                f"Extracted fields - username: {username}, email: {email}, student_id: {student_id}, phone_number: {phone_number}, department_id: {department_id}, gender: {gender}"
            )

            if not username:
                current_app.logger.error("Username is missing")
                return {
                    "status": "error",
                    "message": "사용자명이 필요합니다",
                    "code": "400-01",
                }, 400
            if not email:
                current_app.logger.error("Email is missing")
                return {
                    "status": "error",
                    "message": "이메일이 필요합니다",
                    "code": "400-02",
                }, 400
            if not password:
                current_app.logger.error("Password is missing")
                return {
                    "status": "error",
                    "message": "비밀번호가 필요합니다",
                    "code": "400-03",
                }, 400
            if not student_id:
                current_app.logger.error("Student ID is missing")
                return {
                    "status": "error",
                    "message": "학번이 필요합니다",
                    "code": "400-08",
                }, 400
            if not phone_number:
                current_app.logger.error("Phone number is missing")
                return {
                    "status": "error",
                    "message": "전화번호가 필요합니다",
                    "code": "400-09",
                }, 400
            if not department_id:
                current_app.logger.error("Department ID is missing")
                return {
                    "status": "error",
                    "message": "학과 ID가 필요합니다",
                    "code": "400-12",
                }, 400
            if not gender:
                current_app.logger.error("Gender is missing")
                return {
                    "status": "error",
                    "message": "성별이 필요합니다",
                    "code": "400-13",
                }, 400

            # 3) 상세 형식 검증
            is_valid_username, username_message = validate_username(username)
            if not is_valid_username:
                current_app.logger.error(
                    f"Username validation failed: {username_message}"
                )
                return {
                    "status": "error",
                    "message": username_message,
                    "code": "400-04",
                }, 400

            if not validate_email(email):
                current_app.logger.error(f"Email validation failed: {email}")
                return {
                    "status": "error",
                    "message": "유효하지 않은 이메일 형식입니다.",
                    "code": "400-05",
                }, 400

            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                current_app.logger.error(
                    f"Password validation failed: {password_message}"
                )
                return {
                    "status": "error",
                    "message": password_message,
                    "code": "400-06",
                }, 400

            # 학번과 전화번호 검증
            is_valid_student_id, student_id_message = validate_student_id(student_id)
            if not is_valid_student_id:
                current_app.logger.error(
                    f"Student ID validation failed: {student_id_message}"
                )
                return {
                    "status": "error",
                    "message": student_id_message,
                    "code": "400-10",
                }, 400

            is_valid_phone_number, phone_number_message = validate_phone_number(
                phone_number
            )
            if not is_valid_phone_number:
                current_app.logger.error(
                    f"Phone number validation failed: {phone_number_message}"
                )
                return {
                    "status": "error",
                    "message": phone_number_message,
                    "code": "400-11",
                }, 400

            # 성별 유효성 검증
            valid_genders = ["MALE", "FEMALE", "OTHER"]
            if gender not in valid_genders:
                current_app.logger.error(f"Gender validation failed: {gender}")
                return {
                    "status": "error",
                    "message": "유효하지 않은 성별입니다. MALE, FEMALE, OTHER 중 하나를 선택해주세요.",
                    "code": "400-14",
                }, 400

            # 4) 사용자 생성
            user_data = create_user(
                {
                    "username": username,
                    "email": email,
                    "password": password,
                    "student_id": student_id,
                    "phone_number": phone_number,
                    "department_id": department_id,
                    "gender": gender,
                }
            )

            return {
                "message": "회원가입이 완료되었습니다.",
                "user": user_data,
            }, 201

        except ValueError as e:
            current_app.logger.error(f"ValueError in register: {str(e)}")
            # ValueError는 클라이언트 오류이므로 400으로 처리
            error_message = str(e)
            # 이미 등록된 이메일/학번 등의 경우 구체적인 오류 코드 반환
            if "이미 등록된 이메일입니다." in error_message:
                return {
                    "status": "error",
                    "message": error_message,
                    "code": "400-15",
                }, 400
            elif "이미 등록된 학번입니다." in error_message:
                return {
                    "status": "error",
                    "message": error_message,
                    "code": "400-16",
                }, 400
            else:
                return {
                    "status": "error",
                    "message": error_message,
                    "code": "400-07",
                }, 400
        except Exception as e:
            current_app.logger.exception("auth.register failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class LoginController(Resource):
    """로그인 컨트롤러"""

    def post(self):
        """로그인 API"""
        try:
            # 1) JSON 파싱: 잘못된 JSON이면 BadRequest 유발
            try:
                data = request.get_json(force=False, silent=False)
            except BadRequest:
                return {
                    "status": "error",
                    "message": "유효하지 않은 JSON 형식입니다",
                    "code": "400-00",
                }, 400

            if not isinstance(data, dict):
                return {
                    "status": "error",
                    "message": "JSON 객체가 필요합니다",
                    "code": "400-00",
                }, 400

            # 2) 필드 추출/검증
            email = (data.get("email") or "").strip()
            password = data.get("password")
            channel = (data.get("channel") or "").strip().upper()
            device_id = (data.get("device_id") or "").strip()

            if not email:
                return {
                    "status": "error",
                    "message": "이메일이 필요합니다",
                    "code": "400-01",
                }, 400
            if not password:
                return {
                    "status": "error",
                    "message": "비밀번호가 필요합니다",
                    "code": "400-02",
                }, 400
            if channel not in {"WEB", "APP"}:
                return {
                    "status": "error",
                    "message": "channel은 WEB 또는 APP 이어야 합니다",
                    "code": "400-04",
                }, 400
            if channel == "APP":
                if not device_id:
                    return {
                        "status": "error",
                        "message": "APP 로그인 시 device_id가 필요합니다",
                        "code": "400-05",
                    }, 400
                if len(device_id) > 64:
                    return {
                        "status": "error",
                        "message": "device_id 길이는 64자 이하여야 합니다",
                        "code": "400-06",
                    }, 400
                try:
                    uuid.UUID(device_id)
                except (ValueError, AttributeError):
                    return {
                        "status": "error",
                        "message": "device_id는 UUID 형식이어야 합니다",
                        "code": "400-07",
                    }, 400

            # 3) 사용자 인증
            user_data = authenticate_user(email, password)

            # 4) 세션 생성
            session_data = create_session(
                user_data["user_id"], channel, device_id if channel == "APP" else None
            )

            return {
                "message": "로그인이 완료되었습니다.",
                "user": user_data,
                "session": session_data,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "401-01"}, 401
        except Exception as e:
            current_app.logger.exception("auth.login failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class LogoutController(Resource):
    """로그아웃 컨트롤러"""

    def post(self):
        """로그아웃 API"""
        try:
            # 현재 세션 정보 조회
            current_session = get_current_session()

            if current_session:
                session_id = current_session["session_id"]

                # 세션 비활성화
                deactivate_session(session_id)
            else:
                print("현재 세션이 없습니다")

            # Flask 세션 클리어
            clear_flask_session()
            print("Flask 세션 클리어 완료")

            return {
                "message": "로그아웃이 완료되었습니다.",
            }, 200

        except Exception as e:
            print(f"로그아웃 중 오류 발생: {str(e)}")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class SessionDebugController(Resource):
    """세션 디버깅 컨트롤러"""

    def get(self):
        """비활성화된 디버그 엔드포인트"""
        return {"status": "error", "message": "not found"}, 404


class SessionInfoController(Resource):
    """세션 통합 정보 조회 컨트롤러"""

    def get(self):
        """현재 세션의 통합 정보 조회 API (세션 + 사용자 + 권한 + 동아리)"""
        try:
            from services.session_service import get_session_info

            current_app.logger.info("Starting session info retrieval")

            # 세션 통합 정보 조회
            session_info = get_session_info()

            current_app.logger.info(f"Session info result: {session_info}")

            if not session_info:
                current_app.logger.warning("No session info found - user not logged in")
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            current_app.logger.info("Session info retrieved successfully")
            return {
                "message": "세션 통합 정보를 조회했습니다.",
                "session": session_info,
            }, 200

        except Exception as e:
            current_app.logger.exception("Exception in session-info")
            current_app.logger.error(f"Exception details: {str(e)}")
            current_app.logger.error(f"Exception type: {type(e)}")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class UserListController(Resource):
    """모든 사용자 목록 조회 컨트롤러"""

    def get(self):
        """모든 사용자 정보 조회 API"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 모든 사용자 정보 조회
            users = get_all_users()

            return {
                "message": "모든 사용자 정보를 조회했습니다.",
                "count": len(users),
                "users": users,
            }, 200

        except Exception as e:
            current_app.logger.exception("auth.users failed")
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

from flask_restx import Resource, abort, reqparse
from services.auth_service import (
    create_user,
    authenticate_user,
    validate_username,
    validate_email,
    validate_password
)
from services.session_service import create_session, deactivate_session, clear_flask_session, debug_session_info, get_current_user


class RegisterController(Resource):
    """회원가입 컨트롤러"""

    def post(self):
        """회원가입 API"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("username", type=str, required=True, location="json")
            parser.add_argument("email", type=str, required=True, location="json")
            parser.add_argument("password", type=str, required=True, location="json")
            args = parser.parse_args()

            # 사용자명 형식 검증
            is_valid_username, username_message = validate_username(args['username'])
            if not is_valid_username:
                abort(400, f"400-01: {username_message}")

            # 이메일 형식 검증
            if not validate_email(args['email']):
                abort(400, "400-02: 유효하지 않은 이메일 형식입니다.")

            # 비밀번호 강도 검증
            is_valid_password, password_message = validate_password(args['password'])
            if not is_valid_password:
                abort(400, f"400-03: {password_message}")

            # 사용자 생성
            user_data = create_user({
                'username': args['username'],
                'email': args['email'],
                'password': args['password']
            })

            return {
                "status": "success",
                "message": "회원가입이 완료되었습니다.",
                "data": user_data
            }, 201

        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class LoginController(Resource):
    """로그인 컨트롤러"""

    def post(self):
        """로그인 API"""
        try:
            print(f"\n🔍 [DEBUG] === 로그인 프로세스 시작 ===")
            
            parser = reqparse.RequestParser()
            parser.add_argument("email", type=str, required=True, location="json")
            parser.add_argument("password", type=str, required=True, location="json")
            args = parser.parse_args()

            print(f"🔍 [DEBUG] 로그인 요청 - 이메일: {args['email']}")

            # 사용자 인증
            print(f"🔍 [DEBUG] 사용자 인증 중...")
            user_data = authenticate_user(args['email'], args['password'])
            print(f"🔍 [DEBUG] 사용자 인증 완료: {user_data['name']} (ID: {user_data['user_id']})")
            
            # 세션 생성
            print(f"🔍 [DEBUG] 세션 생성 시작...")
            session_data = create_session(user_data['user_id'])
            print(f"🔍 [DEBUG] 세션 생성 완료: {session_data}")

            # 디버깅 정보 출력
            debug_session_info()

            response_data = {
                "status": "success",
                "message": "로그인이 완료되었습니다.",
                "data": {
                    "user": user_data,
                    "session": session_data
                }
            }
            
            print(f"🔍 [DEBUG] 응답 데이터: {response_data}")
            print(f"🔍 [DEBUG] === 로그인 프로세스 완료 ===\n")

            return response_data, 200

        except ValueError as e:
            print(f"❌ [DEBUG] 로그인 실패 (인증 오류): {str(e)}")
            abort(401, f"401-01: {str(e)}")
        except Exception as e:
            print(f"❌ [DEBUG] 로그인 실패 (서버 오류): {str(e)}")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class LogoutController(Resource):
    """로그아웃 컨트롤러"""

    def post(self):
        """로그아웃 API"""
        try:
            print(f"\n🔍 [DEBUG] === 로그아웃 프로세스 시작 ===")
            
            # 현재 세션 정보 조회
            current_session = get_current_session()
            
            if current_session:
                print(f"🔍 [DEBUG] 현재 세션: {current_session['session_id']}")
                
                # 세션 비활성화
                deactivate_session(current_session['session_id'])
                print(f"🔍 [DEBUG] 세션 비활성화 완료")
            
            # Flask 세션 클리어
            clear_flask_session()
            print(f"🔍 [DEBUG] Flask 세션 클리어 완료")
            
            response_data = {
                "status": "success",
                "message": "로그아웃이 완료되었습니다."
            }
            
            print(f"🔍 [DEBUG] 응답 데이터: {response_data}")
            print(f"🔍 [DEBUG] === 로그아웃 프로세스 완료 ===\n")
            
            return response_data, 200
            
        except Exception as e:
            print(f"❌ [DEBUG] 로그아웃 실패: {str(e)}")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class SessionDebugController(Resource):
    """세션 디버깅 컨트롤러"""

    def get(self):
        """현재 세션 상태 디버깅 정보를 반환합니다"""
        try:
            print(f"\n🔍 [DEBUG] === 세션 디버깅 API 호출 ===")
            debug_session_info()
            
            from services.session_service import get_current_session, get_current_user
            
            current_session = get_current_session()
            current_user = get_current_user()
            
            debug_info = {
                "current_session": current_session,
                "current_user": {
                    "id": current_user.id if current_user else None,
                    "name": current_user.name if current_user else None,
                    "email": current_user.email if current_user else None
                } if current_user else None
            }
            
            print(f"🔍 [DEBUG] 디버깅 정보: {debug_info}")
            print(f"🔍 [DEBUG] === 세션 디버깅 API 완료 ===\n")
            
            return {
                "status": "success",
                "debug_info": debug_info
            }, 200
            
        except Exception as e:
            print(f"❌ [DEBUG] 세션 디버깅 실패: {str(e)}")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class SessionInfoController(Resource):
    """세션 통합 정보 조회 컨트롤러"""

    def get(self):
        """현재 세션의 통합 정보 조회 API (세션 + 사용자 + 권한 + 동아리)"""
        try:
            print(f"\n🔍 [DEBUG] === 세션 통합 정보 조회 시작 ===")
            
            from services.session_service import get_session_info
            
            # 세션 통합 정보 조회
            session_info = get_session_info()
            
            if not session_info:
                print(f"🔍 [DEBUG] 유효한 세션이 없습니다")
                abort(401, "401-01: 로그인이 필요합니다")
            
            response_data = {
                "status": "success",
                "message": "세션 통합 정보를 조회했습니다.",
                "data": session_info
            }
            
            print(f"🔍 [DEBUG] 응답 데이터: {response_data}")
            print(f"🔍 [DEBUG] === 세션 통합 정보 조회 완료 ===\n")
            
            return response_data, 200
            
        except Exception as e:
            print(f"❌ [DEBUG] 세션 통합 정보 조회 실패: {str(e)}")
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

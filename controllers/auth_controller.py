from flask_restx import Resource, abort, reqparse
from services.auth_service import (
    create_user, 
    authenticate_user, 
    validate_email, 
    validate_password, 
    validate_username,
    get_all_users
)


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
            parser = reqparse.RequestParser()
            parser.add_argument("email", type=str, required=True, location="json")
            parser.add_argument("password", type=str, required=True, location="json")
            args = parser.parse_args()

            # 사용자 인증
            user_data = authenticate_user(args['email'], args['password'])

            return {
                "status": "success",
                "message": "로그인이 완료되었습니다.",
                "data": user_data
            }, 200

        except ValueError as e:
            abort(401, f"401-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class UserListController(Resource):
    """사용자 목록 조회 컨트롤러 (테스트용)"""

    def get(self):
        """모든 사용자 목록을 반환합니다"""
        try:
            users_data = get_all_users()
            return {
                "status": "success",
                "count": len(users_data),
                "users": users_data,
            }, 200
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

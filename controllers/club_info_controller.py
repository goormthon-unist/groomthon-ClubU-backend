from flask_restx import Resource, reqparse
from services.session_service import get_current_session
from services.club_info_service import (
    update_club_introduction,
    delete_club_introduction,
    update_club_logo_image,
    delete_club_logo_image,
    update_club_introduction_image,
    delete_club_introduction_image,
    check_club_president_permission,
)


class ClubIntroductionController(Resource):
    """동아리 소개글 관리 컨트롤러"""

    def put(self, club_id):
        """동아리 소개글 업로드/수정"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 요청 데이터 파싱
            parser = reqparse.RequestParser()
            parser.add_argument(
                "introduction", type=str, required=True, location="json"
            )
            args = parser.parse_args()

            # 소개글 업데이트
            result = update_club_introduction(club_id, args["introduction"])

            return {
                "message": "동아리 소개글이 성공적으로 업데이트되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def delete(self, club_id):
        """동아리 소개글 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 소개글 삭제
            result = delete_club_introduction(club_id)

            return {
                "message": "동아리 소개글이 성공적으로 삭제되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class ClubLogoImageController(Resource):
    """동아리 로고 이미지 관리 컨트롤러"""

    def put(self, club_id):
        """동아리 로고 이미지 업로드/수정"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 파일 처리
            from flask import request

            if "image" not in request.files:
                return {
                    "status": "error",
                    "message": "이미지 파일이 필요합니다",
                    "code": "400-02",
                }, 400

            image_file = request.files["image"]
            if image_file.filename == "":
                return {
                    "status": "error",
                    "message": "선택된 파일이 없습니다",
                    "code": "400-03",
                }, 400

            # 로고 이미지 업데이트
            result = update_club_logo_image(club_id, image_file)

            return {
                "message": "동아리 로고 사진이 성공적으로 업데이트되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def delete(self, club_id):
        """동아리 로고 이미지 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 로고 이미지 삭제
            result = delete_club_logo_image(club_id)

            return {
                "message": "동아리 로고 사진이 성공적으로 삭제되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500


class ClubIntroductionImageController(Resource):
    """동아리 소개글 이미지 관리 컨트롤러"""

    def put(self, club_id):
        """동아리 소개글 이미지 업로드/수정"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 파일 처리
            from flask import request

            if "image" not in request.files:
                return {
                    "status": "error",
                    "message": "이미지 파일이 필요합니다",
                    "code": "400-02",
                }, 400

            image_file = request.files["image"]
            if image_file.filename == "":
                return {
                    "status": "error",
                    "message": "선택된 파일이 없습니다",
                    "code": "400-03",
                }, 400

            # 소개글 이미지 업데이트
            result = update_club_introduction_image(club_id, image_file)

            return {
                "message": "동아리 소개글 사진이 성공적으로 업데이트되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

    def delete(self, club_id):
        """동아리 소개글 이미지 삭제"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # 회장 권한 확인
            user_id = session_data["user_id"]
            check_club_president_permission(user_id, club_id)

            # 소개글 이미지 삭제
            result = delete_club_introduction_image(club_id)

            return {
                "message": "동아리 소개글 사진이 성공적으로 삭제되었습니다.",
                "club": result,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {e}",
                "code": "500-00",
            }, 500

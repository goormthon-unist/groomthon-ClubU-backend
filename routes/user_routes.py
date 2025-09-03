from flask_restx import Namespace
from controllers.user_controller import (
    UserProfileController,
    UserClubsController,
    UserApplicationsController,
)

# 네임스페이스 생성
user_ns = Namespace("users", description="사용자 관리 API")


# API 엔드포인트 등록
@user_ns.route("/me")
class UserProfileResource(UserProfileController):
    """마이페이지 사용자 정보 조회 리소스"""

    @user_ns.doc("get_user_profile")
    @user_ns.response(200, "사용자 프로필 조회 성공")
    @user_ns.response(401, "로그인이 필요합니다")
    @user_ns.response(404, "사용자를 찾을 수 없습니다")
    @user_ns.response(500, "서버 내부 오류")
    def get(self):
        """현재 로그인한 사용자의 프로필 정보를 조회합니다"""
        return super().get()


@user_ns.route("/me/clubs")
class UserClubsResource(UserClubsController):
    """내가 속한 동아리 목록 조회 리소스"""

    @user_ns.doc("get_user_clubs")
    @user_ns.response(200, "사용자 동아리 목록 조회 성공")
    @user_ns.response(401, "로그인이 필요합니다")
    @user_ns.response(500, "서버 내부 오류")
    def get(self):
        """현재 로그인한 사용자가 속한 동아리 목록을 조회합니다"""
        return super().get()


@user_ns.route("/me/applications")
class UserApplicationsResource(UserApplicationsController):
    """내가 지원한 동아리 지원서 목록 조회 리소스 (SUBMITTED 상태만)"""

    @user_ns.doc("get_user_applications")
    @user_ns.response(200, "사용자 지원서 목록 조회 성공")
    @user_ns.response(401, "로그인이 필요합니다")
    @user_ns.response(500, "서버 내부 오류")
    def get(self):
        """현재 로그인한 사용자가 지원한 동아리 지원서 목록을 조회합니다 (SUBMITTED 상태만)"""
        return super().get()

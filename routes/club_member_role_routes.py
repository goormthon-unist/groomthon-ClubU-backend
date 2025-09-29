"""
동아리 멤버 권한 관리 라우트
동아리 회장이 자신의 동아리 내에서만 멤버 권한을 변경할 수 있도록 제한
"""

from flask_restx import Namespace, fields
from controllers.club_member_role_controller import (
    ClubMemberRegistrationController,
    ClubMemberRoleChangeController,
    ClubMemberRolesController,
    ClubAvailableRolesController,
    ClubMembersListController,
)

# 네임스페이스 정의
club_member_role_ns = Namespace("clubs", description="동아리 멤버 권한 관리 API")

# Request Body 모델 정의
club_member_registration_model = club_member_role_ns.model(
    "ClubMemberRegistration",
    {
        "student_id": fields.String(required=True, description="학번"),
        "name": fields.String(required=True, description="이름"),
        "role_name": fields.String(
            required=True,
            description="역할명 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT, CLUB_MEMBER_REST, STUDENT)",
            enum=[
                "CLUB_MEMBER",
                "CLUB_OFFICER",
                "CLUB_PRESIDENT",
                "CLUB_MEMBER_REST",
                "STUDENT",
            ],
        ),
        "generation": fields.Integer(required=False, description="기수 (선택사항)"),
        "other_info": fields.String(required=False, description="기타 정보 (선택사항)"),
    },
)

club_member_role_change_model = club_member_role_ns.model(
    "ClubMemberRoleChange",
    {
        "role_name": fields.String(
            required=True,
            description="새로운 역할명 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT, CLUB_MEMBER_REST, STUDENT)",
            enum=[
                "CLUB_MEMBER",
                "CLUB_OFFICER",
                "CLUB_PRESIDENT",
                "CLUB_MEMBER_REST",
                "STUDENT",
            ],
        ),
        "generation": fields.Integer(required=False, description="기수 (선택사항)"),
        "other_info": fields.String(required=False, description="기타 정보 (선택사항)"),
    },
)


# 라우트 등록
@club_member_role_ns.route("/<int:club_id>/members")
class ClubMemberRegistrationResource(ClubMemberRegistrationController):
    """동아리 멤버 직접 등록 리소스"""

    @club_member_role_ns.doc("register_club_member")
    @club_member_role_ns.expect(club_member_registration_model)
    @club_member_role_ns.response(201, "멤버 등록 성공")
    @club_member_role_ns.response(400, "잘못된 요청")
    @club_member_role_ns.response(401, "로그인이 필요합니다")
    @club_member_role_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @club_member_role_ns.response(500, "서버 내부 오류")
    def post(self, club_id):
        """
        개선된 동아리 멤버 등록 (학번과 이름으로 검색)

        요청 본문:
        {
            "student_id": "20240001",          // 학번 (필수)
            "name": "김지원",                  // 이름 (필수)
            "role_name": "CLUB_MEMBER",        // 역할명 (필수): CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT, CLUB_MEMBER_REST, STUDENT
            "generation": 1,                   // 기수 (선택사항)
            "other_info": "신입"               // 기타 정보 (선택사항)
        }

        예시:
        - 일반 멤버 등록: {"student_id": "20240001", "name": "김지원", "role_name": "CLUB_MEMBER"}
        - 휴동중 처리: {"student_id": "20240001", "name": "김지원", "role_name": "CLUB_MEMBER_REST", "other_info": "군입대"}
        - 탈퇴 처리: {"student_id": "20240001", "name": "김지원", "role_name": "STUDENT", "other_info": "개인사정"}
        """
        return super().post(club_id)


@club_member_role_ns.route("/<int:club_id>/members/roles")
class ClubMembersListResource(ClubMembersListController):
    """동아리 멤버 목록 조회 리소스"""

    @club_member_role_ns.doc("get_club_members_list")
    @club_member_role_ns.response(200, "멤버 목록 조회 성공")
    @club_member_role_ns.response(401, "로그인이 필요합니다")
    @club_member_role_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    def get(self, club_id):
        """
        동아리 멤버 목록 조회 (역할별 정렬)

        동아리 회장이 자신의 동아리 멤버들을 역할별로 정렬하여 조회합니다.
        """
        return super().get(club_id)


@club_member_role_ns.route("/<int:club_id>/members/<int:user_id>/role")
class ClubMemberRoleResource(ClubMemberRoleChangeController, ClubMemberRolesController):
    """동아리 멤버 권한 관리 리소스 (변경 + 조회)"""

    @club_member_role_ns.doc("change_club_member_role")
    @club_member_role_ns.expect(club_member_role_change_model)
    @club_member_role_ns.response(200, "권한 변경 성공")
    @club_member_role_ns.response(400, "잘못된 요청")
    @club_member_role_ns.response(401, "로그인이 필요합니다")
    @club_member_role_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    @club_member_role_ns.response(500, "서버 내부 오류")
    def post(self, club_id, user_id):
        """
        동아리 멤버 권한 변경

        요청 본문:
        {
            "role_name": "CLUB_OFFICER",       // 새로운 역할명 (필수): CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT, CLUB_MEMBER_REST, STUDENT
            "generation": 2,                   // 기수 (선택사항)
            "other_info": "기획부장"           // 기타 정보 (선택사항)
        }

        예시:
        - 멤버를 간부로 승격: {"role_name": "CLUB_OFFICER"}
        - 휴동중으로 변경: {"role_name": "CLUB_MEMBER_REST", "other_info": "군입대"}
        - 탈퇴 처리: {"role_name": "STUDENT", "other_info": "개인사정"}
        """
        return ClubMemberRoleChangeController.post(self, club_id, user_id)

    @club_member_role_ns.doc("get_club_member_roles")
    @club_member_role_ns.response(200, "권한 조회 성공")
    @club_member_role_ns.response(401, "로그인이 필요합니다")
    @club_member_role_ns.response(403, "CLUB_PRESIDENT 권한이 필요합니다")
    def get(self, club_id, user_id):
        """
        동아리 멤버 권한 조회

        특정 사용자의 동아리 내 권한 정보를 조회합니다.
        """
        return ClubMemberRolesController.get(self, club_id, user_id)


@club_member_role_ns.route("/roles")
class ClubAvailableRolesResource(ClubAvailableRolesController):
    """동아리 사용 가능한 역할 조회 리소스"""

    @club_member_role_ns.doc("get_available_roles")
    @club_member_role_ns.response(200, "역할 목록 조회 성공")
    def get(self):
        """
        동아리에서 사용 가능한 역할 목록 조회

        동아리 내에서 설정할 수 있는 역할들을 조회합니다.
        """
        return super().get()

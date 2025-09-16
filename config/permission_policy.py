"""
권한 정책 중앙 관리 파일
모든 API 엔드포인트의 권한 설정을 한 곳에서 관리
"""

# 권한 레벨 정의
ROLE_HIERARCHY = {
    "STUDENT": 1,
    "CLUB_MEMBER": 2,
    "CLUB_OFFICER": 3,
    "CLUB_PRESIDENT": 4,
    "UNION_ADMIN": 5,
    "DEVELOPER": 6,
}

# API 엔드포인트별 권한 정책
# 기본: 모든 API는 'STUDENT' 권한으로 접근 가능
# 예외: 아래 명시된 API들만 특정 권한 필요

PERMISSION_POLICY = {
    # ===== CLUB_PRESIDENT만 접근 가능한 API들 =====
    "clubs.update": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "동아리 정보 수정 (PATCH /api/v1/clubs/{club_id})",
    },
    "clubs.status": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "동아리 상태 관리 (PATCH /api/v1/clubs/{club_id}/status)",
    },
    "clubs.application_questions_create": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "동아리 지원서 질문 생성 (POST /api/v1/clubs/{club_id}/application/questions)",
    },
    "application_questions.update": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "지원서 질문 수정 (PATCH /api/v1/application/questions/{question_id})",
    },
    "application_questions.delete": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "지원서 질문 삭제 (DELETE /api/v1/application/questions/{question_id})",
    },
    "applications.list_by_club": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "동아리별 지원서 목록 조회 (GET /api/v1/applications?club_id={id})",
    },
    "applications.detail": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "지원서 상세 조회 (GET /api/v1/applications/{application_id})",
    },
    "members.create": {
        "allowed_roles": {"CLUB_PRESIDENT", "DEVELOPER"},
        "description": "멤버 등록 (POST /api/v1/members)",
    },
    # ===== CLUB_MEMBER만 접근 가능한 API들 =====
    "clubs.members_read": {
        "allowed_roles": {"CLUB_MEMBER", "DEVELOPER"},
        "description": "동아리 멤버 목록 조회 (GET /api/v1/clubs/{club_id}/members)",
    },
    "notices.club_list_read": {
        "allowed_roles": {"CLUB_MEMBER", "DEVELOPER"},
        "description": "클럽 공지사항 목록 조회 (GET /api/v1/clubs/{club_id}/notices)",
    },
    # ===== CLUB_PRESIDENT + UNION_ADMIN + DEVELOPER 모두 접근 가능한 API들 =====
    "clubs.members": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "동아리 멤버 목록 조회 (GET /api/v1/clubs/{club_id}/members)",
    },
    "notices.club_create": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "클럽 공지사항 작성 (POST /api/v1/clubs/{id}/notices)",
    },
    "notices.club_update": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "클럽 공지사항 수정 (PATCH /api/v1/clubs/{id}/notices/{notice_id})",
    },
    "notices.club_delete": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "클럽 공지사항 삭제 (DELETE /api/v1/clubs/{id}/notices/{notice_id})",
    },
    "notices.club_list": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "클럽 공지사항 목록 조회 (GET /api/v1/clubs/{club_id}/notices)",
    },
    "banners.create": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "배너 생성 (POST /api/v1/banners)",
    },
    "banners.delete": {
        "allowed_roles": {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"},
        "description": "배너 삭제 (DELETE /api/v1/banners/{id})",
    },
    # ===== UNION_ADMIN만 접근 가능한 API들 =====
    "banners.update_status": {
        "allowed_roles": {"UNION_ADMIN", "DEVELOPER"},
        "description": "배너 상태 수정 (PATCH /api/v1/banners/{id}/status)",
    },
    # ===== DEVELOPER만 접근 가능한 API들 =====
    "admin.user_role_change": {
        "allowed_roles": {"DEVELOPER"},
        "description": "사용자 권한 변경 (POST /api/v1/admin/users/{user_id}/roles)",
    },
}


def get_permission_policy(permission_key):
    """권한 정책 조회"""
    return PERMISSION_POLICY.get(permission_key)


def get_all_permissions():
    """모든 권한 정책 조회 (관리용)"""
    return PERMISSION_POLICY


def is_role_higher_or_equal(role1, role2):
    """역할 계층 비교 (role1이 role2보다 높거나 같은지)"""
    level1 = ROLE_HIERARCHY.get(role1, 0)
    level2 = ROLE_HIERARCHY.get(role2, 0)
    return level1 >= level2

"""
권한 시스템 테스트
"""

import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from config.permission_policy import get_permission_policy, ROLE_HIERARCHY
from services.permission_service import PermissionService


@pytest.fixture
def client():
    """테스트용 Flask 클라이언트"""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def app():
    """테스트용 Flask 앱"""
    app = create_app()
    app.config["TESTING"] = True
    return app


class TestPermissionPolicy:
    """권한 정책 테스트"""

    def test_permission_policy_retrieval(self):
        """권한 정책 조회 테스트"""
        # 존재하는 권한 정책 조회
        policy = get_permission_policy("clubs.update")
        assert policy is not None
        assert "allowed_roles" in policy
        assert "description" in policy
        assert "CLUB_PRESIDENT" in policy["allowed_roles"]
        assert "DEVELOPER" in policy["allowed_roles"]

        # 여러 권한이 필요한 API 테스트
        policy = get_permission_policy("notices.club_create")
        assert policy is not None
        assert "CLUB_PRESIDENT" in policy["allowed_roles"]
        assert "UNION_ADMIN" in policy["allowed_roles"]
        assert "DEVELOPER" in policy["allowed_roles"]

        # 존재하지 않는 권한 정책
        policy = get_permission_policy("nonexistent.permission")
        assert policy is None

    def test_role_hierarchy(self):
        """역할 계층 테스트"""
        assert ROLE_HIERARCHY["STUDENT"] == 1
        assert ROLE_HIERARCHY["CLUB_MEMBER"] == 2
        assert ROLE_HIERARCHY["CLUB_OFFICER"] == 3
        assert ROLE_HIERARCHY["CLUB_PRESIDENT"] == 4
        assert ROLE_HIERARCHY["UNION_ADMIN"] == 5
        assert ROLE_HIERARCHY["DEVELOPER"] == 6


class TestPermissionService:
    """권한 서비스 테스트"""

    def test_permission_service_initialization(self):
        """권한 서비스 초기화 테스트"""
        service = PermissionService()
        assert service is not None
        assert hasattr(service, "check_permission")
        assert hasattr(service, "get_user_roles")

    @patch("services.session_service.get_current_user")
    def test_permission_check_without_user(self, mock_get_current_user):
        """사용자 없이 권한 검사 테스트"""
        mock_get_current_user.return_value = None

        service = PermissionService()
        result = service.check_permission("clubs.update")

        assert result["has_permission"] is False
        assert result["message"] == "로그인이 필요합니다"
        assert result["user_id"] is None

    @patch("services.session_service.get_current_user")
    @patch("models.db.session.query")
    def test_permission_check_with_user(self, mock_query, mock_get_current_user):
        """사용자와 함께 권한 검사 테스트"""
        # Mock 사용자
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user

        # Mock DB 쿼리 결과 (CLUB_PRESIDENT 권한을 가진 사용자)
        mock_membership = MagicMock()
        mock_role = MagicMock()
        mock_role.role_name = "CLUB_PRESIDENT"
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = [
            (mock_membership, mock_role)
        ]

        service = PermissionService()
        result = service.check_permission("clubs.update")

        assert result["has_permission"] is True
        assert result["user_id"] == 1
        assert "CLUB_PRESIDENT" in result["user_roles"]

    @patch("services.session_service.get_current_user")
    @patch("models.db.session.query")
    def test_permission_check_insufficient_permission(
        self, mock_query, mock_get_current_user
    ):
        """권한 부족 테스트"""
        # Mock 사용자
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user

        # Mock DB 쿼리 결과 (STUDENT 권한만 가진 사용자)
        mock_membership = MagicMock()
        mock_role = MagicMock()
        mock_role.role_name = "STUDENT"
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = [
            (mock_membership, mock_role)
        ]

        service = PermissionService()
        result = service.check_permission("clubs.update")

        assert result["has_permission"] is False
        assert result["user_id"] == 1
        assert "STUDENT" in result["user_roles"]
        assert "CLUB_PRESIDENT" in result["required_roles"]

    def test_permission_info_retrieval(self):
        """권한 정보 조회 테스트"""
        service = PermissionService()

        # 존재하는 권한 정보 조회
        info = service.get_permission_info("clubs.update")
        assert "permission_key" in info
        assert "description" in info
        assert "required_roles" in info
        assert "role_hierarchy" in info
        assert info["permission_key"] == "clubs.update"

        # 존재하지 않는 권한 정보 조회
        info = service.get_permission_info("nonexistent.permission")
        assert "error" in info


class TestPermissionDecorator:
    """권한 데코레이터 테스트"""

    def test_decorator_import(self):
        """데코레이터 import 테스트"""
        from utils.permission_decorator import (
            require_permission,
            require_any_permission,
            require_all_permissions,
            optional_permission,
        )

        assert require_permission is not None
        assert require_any_permission is not None
        assert require_all_permissions is not None
        assert optional_permission is not None

    def test_decorator_functionality(self):
        """데코레이터 기능 테스트"""
        from utils.permission_decorator import require_permission

        # 데코레이터가 함수를 반환하는지 확인
        @require_permission("clubs.update")
        def test_function():
            return "success"

        assert callable(test_function)
        assert test_function.__name__ == "test_function"


class TestPermissionIntegration:
    """권한 시스템 통합 테스트"""

    def test_permission_combinations(self):
        """권한 조합 테스트"""
        # 여러 권한이 필요한 API들 테스트
        test_cases = [
            ("clubs.members", {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"}),
            ("notices.club_create", {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"}),
            ("banners.create", {"CLUB_PRESIDENT", "UNION_ADMIN", "DEVELOPER"}),
            ("banners.update_status", {"UNION_ADMIN", "DEVELOPER"}),
            ("admin.user_role_change", {"DEVELOPER"}),
        ]

        for permission_key, expected_roles in test_cases:
            policy = get_permission_policy(permission_key)
            assert policy is not None
            assert policy["allowed_roles"] == expected_roles

    def test_default_student_permission(self):
        """기본 STUDENT 권한 테스트"""
        # 권한 정책이 없는 경우 기본 STUDENT 권한이 적용되는지 확인
        service = PermissionService()

        # Mock을 사용하여 권한 정책이 없는 경우 테스트
        with patch("config.permission_policy.get_permission_policy", return_value=None):
            with patch("services.session_service.get_current_user", return_value=None):
                result = service.check_permission("nonexistent.permission")
                assert result["required_roles"] == {"STUDENT"}

    def test_club_context_permission(self):
        """동아리 컨텍스트 권한 검사 테스트"""
        # 동아리 컨텍스트 파라미터가 제대로 전달되는지 확인
        service = PermissionService()

        # check_permission 메서드가 club_id 파라미터를 받는지 확인
        import inspect

        sig = inspect.signature(service.check_permission)
        assert "club_id" in sig.parameters


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

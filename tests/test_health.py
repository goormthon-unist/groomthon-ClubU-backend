"""
헬스체크 엔드포인트 테스트
"""
import pytest
from app import create_app


@pytest.fixture
def client():
    """테스트용 Flask 클라이언트"""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """헬스체크 엔드포인트 테스트"""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert "message" in data
    assert "database" in data


def test_root_endpoint(client):
    """루트 엔드포인트 테스트"""
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

#!/usr/bin/env python3
"""
세션 인증 테스트 스크립트
DB 없이 세션 인증 로직만 테스트
"""

import requests
import json
from datetime import datetime

# 테스트용 Mock 세션 데이터
MOCK_SESSION = {
    "session_id": "test-session-123",
    "user_id": 101,
    "expires_at": "2024-12-31T23:59:59",
}


def test_session_auth():
    """세션 인증이 필요한 API들을 테스트"""

    base_url = "http://localhost:5000/api/v1"

    # 테스트할 API 엔드포인트들
    test_endpoints = [
        # 사용자 관련 API
        {"method": "GET", "url": f"{base_url}/users/me", "name": "사용자 프로필 조회"},
        {
            "method": "GET",
            "url": f"{base_url}/users/me/clubs",
            "name": "내 동아리 목록",
        },
        {
            "method": "GET",
            "url": f"{base_url}/users/me/applications",
            "name": "내 지원서 목록",
        },
        # 동아리 관리 API
        {"method": "PATCH", "url": f"{base_url}/clubs/1", "name": "동아리 정보 수정"},
        {
            "method": "PATCH",
            "url": f"{base_url}/clubs/1/status",
            "name": "동아리 모집상태 변경",
        },
        # 지원서 관리 API
        {
            "method": "GET",
            "url": f"{base_url}/applications?club_id=1",
            "name": "지원자 목록 조회",
        },
        {
            "method": "GET",
            "url": f"{base_url}/applications/1",
            "name": "지원서 상세 조회",
        },
        {"method": "POST", "url": f"{base_url}/members", "name": "동아리원 등록"},
        # 공지 관리 API
        {
            "method": "POST",
            "url": f"{base_url}/clubs/1/notices",
            "name": "동아리 공지 등록",
        },
        {
            "method": "PATCH",
            "url": f"{base_url}/clubs/1/notices/1",
            "name": "동아리 공지 수정",
        },
        {
            "method": "DELETE",
            "url": f"{base_url}/clubs/1/notices/1",
            "name": "동아리 공지 삭제",
        },
        # 배너 관리 API
        {"method": "POST", "url": f"{base_url}/banners/", "name": "배너 등록"},
        {
            "method": "PATCH",
            "url": f"{base_url}/banners/1/status",
            "name": "배너 상태 변경",
        },
        {"method": "DELETE", "url": f"{base_url}/banners/1", "name": "배너 삭제"},
    ]

    print("🔐 세션 인증 테스트 시작")
    print("=" * 50)

    # 세션 없이 테스트 (401 에러 예상)
    print("\n❌ 세션 없이 테스트 (401 에러 예상)")
    for endpoint in test_endpoints[:3]:  # 처음 3개만 테스트
        try:
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"])
            elif endpoint["method"] == "POST":
                response = requests.post(endpoint["url"], json={})
            elif endpoint["method"] == "PATCH":
                response = requests.patch(endpoint["url"], json={})
            elif endpoint["method"] == "DELETE":
                response = requests.delete(endpoint["url"])

            print(f"  {endpoint['name']}: {response.status_code}")
            if response.status_code == 401:
                print(f"    ✅ 예상대로 401 에러 발생")
            else:
                print(f"    ❌ 예상과 다른 응답: {response.text[:100]}")

        except requests.exceptions.ConnectionError:
            print(f"  {endpoint['name']}: 서버 연결 실패 (서버가 실행 중이지 않음)")
        except Exception as e:
            print(f"  {endpoint['name']}: 오류 - {str(e)}")

    print("\n" + "=" * 50)
    print("✅ 세션 인증 테스트 완료")
    print("\n💡 참고사항:")
    print("- 401 에러가 나오면 세션 인증이 정상적으로 작동하는 것입니다")
    print("- 서버가 실행 중이지 않으면 연결 실패 메시지가 나옵니다")
    print("- DB 연결 오류는 정상입니다 (테스트 목적)")


if __name__ == "__main__":
    test_session_auth()

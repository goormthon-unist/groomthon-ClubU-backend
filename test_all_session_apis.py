#!/usr/bin/env python3
"""
모든 세션 인증 API 테스트 스크립트
새로 추가한 16개 API 포함 전체 테스트
"""

import requests
import json
from datetime import datetime


def test_all_session_apis():
    """모든 세션 인증이 필요한 API들을 테스트"""

    base_url = "http://localhost:5000/api/v1"

    # 새로 추가한 16개 API + 기존 API들
    test_endpoints = [
        # 1. 지원서 제출
        {
            "method": "POST",
            "url": f"{base_url}/applications/1",
            "name": "지원서 제출",
            "data": {"answers": [{"question_id": 1, "answer_text": "테스트 답변"}]},
        },
        # 2. 질문 응답 제출 (아직 구현되지 않음)
        # {"method": "POST", "url": f"{base_url}/recommendation/submit", "name": "질문 응답 제출"},
        # 3. 동아리 정보 수정
        {
            "method": "PATCH",
            "url": f"{base_url}/clubs/1",
            "name": "동아리 정보 수정",
            "data": {"name": "테스트 동아리"},
        },
        # 4. 동아리 모집상태 변경
        {
            "method": "PATCH",
            "url": f"{base_url}/clubs/1/status",
            "name": "동아리 모집상태 변경",
            "data": {"status": "RECRUITING"},
        },
        # 5. 지원서 문항 추가
        {
            "method": "POST",
            "url": f"{base_url}/clubs/1/application/questions",
            "name": "지원서 문항 추가",
            "data": {"question_text": "테스트 질문"},
        },
        # 6. 지원서 문항 수정
        {
            "method": "PATCH",
            "url": f"{base_url}/application/questions/1",
            "name": "지원서 문항 수정",
            "data": {"question_text": "수정된 질문"},
        },
        # 7. 지원서 문항 삭제
        {
            "method": "DELETE",
            "url": f"{base_url}/application/questions/1",
            "name": "지원서 문항 삭제",
        },
        # 8. 지원서 지원자 리스트
        {
            "method": "GET",
            "url": f"{base_url}/applications?club_id=1",
            "name": "지원서 지원자 리스트",
        },
        # 9. 지원서 상세 조회
        {
            "method": "GET",
            "url": f"{base_url}/applications/1",
            "name": "지원서 상세 조회",
        },
        # 10. 동아리원 등록
        {
            "method": "POST",
            "url": f"{base_url}/members",
            "name": "동아리원 등록",
            "data": {"application_id": 1, "role_id": 1},
        },
        # 11. 동아리원 목록 조회
        {
            "method": "GET",
            "url": f"{base_url}/clubs/1/members",
            "name": "동아리원 목록 조회",
        },
        # 12. 동아리 공지 등록
        {
            "method": "POST",
            "url": f"{base_url}/clubs/1/notices",
            "name": "동아리 공지 등록",
            "data": {"title": "테스트 공지", "content": "테스트 내용"},
        },
        # 13. 동아리 공지 수정
        {
            "method": "PATCH",
            "url": f"{base_url}/clubs/1/notices/1",
            "name": "동아리 공지 수정",
            "data": {"title": "수정된 공지"},
        },
        # 14. 동아리 공지 삭제
        {
            "method": "DELETE",
            "url": f"{base_url}/clubs/1/notices/1",
            "name": "동아리 공지 삭제",
        },
        # 15. 배너 등록
        {
            "method": "POST",
            "url": f"{base_url}/banners/",
            "name": "배너 등록",
            "data": {"club_id": 1, "title": "테스트 배너"},
        },
        # 16. 배너 상태 변경
        {
            "method": "PATCH",
            "url": f"{base_url}/banners/1/status",
            "name": "배너 상태 변경",
            "data": {"status": "ACTIVE"},
        },
        # 17. 배너 삭제
        {"method": "DELETE", "url": f"{base_url}/banners/1", "name": "배너 삭제"},
        # 기존 API들
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
        {"method": "POST", "url": f"{base_url}/auth/logout", "name": "로그아웃"},
        {
            "method": "GET",
            "url": f"{base_url}/auth/session-info",
            "name": "세션 정보 조회",
        },
    ]

    print("🔐 전체 세션 인증 API 테스트 시작")
    print("=" * 60)

    success_count = 0
    total_count = len(test_endpoints)

    for i, endpoint in enumerate(test_endpoints, 1):
        try:
            # 요청 데이터 준비
            data = endpoint.get("data", {})

            # HTTP 요청 실행
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"])
            elif endpoint["method"] == "POST":
                response = requests.post(endpoint["url"], json=data)
            elif endpoint["method"] == "PATCH":
                response = requests.patch(endpoint["url"], json=data)
            elif endpoint["method"] == "DELETE":
                response = requests.delete(endpoint["url"])

            # 결과 확인
            if response.status_code == 401:
                print(f"✅ {i:2d}. {endpoint['name']}: 401 (정상)")
                success_count += 1
            else:
                print(
                    f"❌ {i:2d}. {endpoint['name']}: {response.status_code} (예상: 401)"
                )
                if response.status_code != 500:  # DB 오류는 무시
                    print(f"    응답: {response.text[:100]}")

        except requests.exceptions.ConnectionError:
            print(f"🔌 {i:2d}. {endpoint['name']}: 서버 연결 실패")
        except Exception as e:
            print(f"⚠️  {i:2d}. {endpoint['name']}: 오류 - {str(e)}")

    print("\n" + "=" * 60)
    print(f"📊 테스트 결과: {success_count}/{total_count} 성공")

    if success_count == total_count:
        print("🎉 모든 API에서 세션 인증이 정상적으로 작동합니다!")
    else:
        print("⚠️  일부 API에서 예상과 다른 결과가 나왔습니다.")

    print("\n💡 참고사항:")
    print("- 401 에러가 나오면 세션 인증이 정상적으로 작동하는 것입니다")
    print("- 500 에러는 DB 연결 오류로 정상입니다 (테스트 목적)")
    print("- 서버가 실행 중이지 않으면 연결 실패 메시지가 나옵니다")


if __name__ == "__main__":
    test_all_session_apis()

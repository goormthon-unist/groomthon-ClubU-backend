#!/usr/bin/env python3
"""
배포된 서버에서 마이페이지 API 테스트
1. 회원가입
2. 로그인  
3. 마이페이지 3개 API 테스트
"""

import requests
import json
from datetime import datetime
import uuid

# 배포된 서버 URL
BASE_URL = "https://api.clubu.co.kr"


def print_response(title, response):
    """응답을 예쁘게 출력"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")

    try:
        data = response.json()
        print(f"Response Body:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Response Text: {response.text}")
        print(f"JSON Parse Error: {e}")


def test_production_mypage():
    """배포된 서버에서 마이페이지 테스트"""

    # 세션 유지를 위한 requests.Session 사용
    session = requests.Session()

    # 고유한 테스트 사용자 생성
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_student_id = f"2024{unique_id[:4]}"

    print("🚀 배포된 서버에서 마이페이지 테스트 시작...")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    print(f"Test Email: {test_email}")

    # 1. 회원가입 테스트
    print(f"\n{'='*60}")
    print("1️⃣ 회원가입 테스트")
    print(f"{'='*60}")

    register_data = {
        "username": test_username,
        "email": test_email,
        "password": "Test123!@#",
        "student_id": test_student_id,
        "phone_number": "010-1234-5678",
    }

    try:
        response = session.post(
            f"{BASE_URL}/api/v1/auth/register", json=register_data, timeout=30
        )
        print_response("회원가입", response)

        if response.status_code != 201:
            print("❌ 회원가입 실패! 테스트를 중단합니다.")
            return

        print("✅ 회원가입 성공!")

    except Exception as e:
        print(f"❌ 회원가입 요청 실패: {e}")
        return

    # 2. 로그인 테스트
    print(f"\n{'='*60}")
    print("2️⃣ 로그인 테스트")
    print(f"{'='*60}")

    login_data = {"email": test_email, "password": "Test123!@#"}

    try:
        response = session.post(
            f"{BASE_URL}/api/v1/auth/login", json=login_data, timeout=30
        )
        print_response("로그인", response)

        if response.status_code != 200:
            print("❌ 로그인 실패! 테스트를 중단합니다.")
            return

        print("✅ 로그인 성공!")

    except Exception as e:
        print(f"❌ 로그인 요청 실패: {e}")
        return

    # 3. 마이페이지 사용자 정보 조회
    print(f"\n{'='*60}")
    print("3️⃣ 마이페이지 - 사용자 정보 조회")
    print(f"{'='*60}")

    try:
        response = session.get(f"{BASE_URL}/api/v1/users/me", timeout=30)
        print_response("사용자 프로필", response)

        if response.status_code == 200:
            print("✅ 사용자 프로필 조회 성공!")
        else:
            print("❌ 사용자 프로필 조회 실패")

    except Exception as e:
        print(f"❌ 사용자 프로필 조회 실패: {e}")

    # 4. 내가 속한 동아리 목록
    print(f"\n{'='*60}")
    print("4️⃣ 마이페이지 - 내가 속한 동아리 목록")
    print(f"{'='*60}")

    try:
        response = session.get(f"{BASE_URL}/api/v1/users/me/clubs", timeout=30)
        print_response("동아리 목록", response)

        if response.status_code == 200:
            print("✅ 동아리 목록 조회 성공!")
        else:
            print("❌ 동아리 목록 조회 실패")

    except Exception as e:
        print(f"❌ 동아리 목록 조회 실패: {e}")

    # 5. 내가 지원한 지원서 목록
    print(f"\n{'='*60}")
    print("5️⃣ 마이페이지 - 내가 지원한 지원서 목록")
    print(f"{'='*60}")

    try:
        response = session.get(f"{BASE_URL}/api/v1/users/me/applications", timeout=30)
        print_response("지원서 목록", response)

        if response.status_code == 200:
            print("✅ 지원서 목록 조회 성공!")
        else:
            print("❌ 지원서 목록 조회 실패")

    except Exception as e:
        print(f"❌ 지원서 목록 조회 실패: {e}")

    # 6. 로그아웃 (선택사항)
    print(f"\n{'='*60}")
    print("6️⃣ 로그아웃 테스트")
    print(f"{'='*60}")

    try:
        response = session.post(f"{BASE_URL}/api/v1/auth/logout", timeout=30)
        print_response("로그아웃", response)

        if response.status_code == 200:
            print("✅ 로그아웃 성공!")
        else:
            print("❌ 로그아웃 실패")

    except Exception as e:
        print(f"❌ 로그아웃 실패: {e}")

    print(f"\n{'='*60}")
    print("🎉 모든 마이페이지 테스트 완료!")
    print(f"{'='*60}")


if __name__ == "__main__":
    test_production_mypage()

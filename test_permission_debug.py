#!/usr/bin/env python3
"""
권한 디버깅 테스트 스크립트
로그인 후 세션을 통한 권한 확인을 테스트합니다.
"""

import requests
import json

# 서버 설정
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
LOGOUT_URL = f"{BASE_URL}/api/v1/auth/logout"
DEBUG_URL = f"{BASE_URL}/api/v1/auth/debug/session"

# 권한 관련 API
MY_CLUBS_URL = f"{BASE_URL}/api/v1/roles/my-clubs"
PERMISSION_URL = f"{BASE_URL}/api/v1/roles/clubs/{{club_id}}/my-permission"


def test_permission_flow():
    """권한 확인 전체 플로우 테스트"""
    print("🔍 [TEST] === 권한 디버깅 테스트 시작 ===")

    # 1. 로그인
    print("\n1️⃣ 로그인...")
    login_data = {"email": "tkfkd@unist.ac.kr", "password": "password123"}

    response = requests.post(LOGIN_URL, json=login_data)
    print(f"🔍 [TEST] 로그인 응답: {response.status_code}")

    if response.status_code != 200:
        print("❌ [TEST] 로그인 실패")
        return

    # 쿠키 저장
    cookies = response.cookies
    print(f"🔍 [TEST] 쿠키 획득: {dict(cookies)}")

    # 2. 세션 디버깅 정보 확인
    print("\n2️⃣ 세션 상태 확인...")
    debug_response = requests.get(DEBUG_URL, cookies=cookies)
    print(f"🔍 [TEST] 세션 디버깅 응답: {debug_response.status_code}")

    if debug_response.status_code == 200:
        debug_data = debug_response.json()
        print(f"🔍 [TEST] 세션 정보:")
        print(json.dumps(debug_data, indent=2, ensure_ascii=False))

    # 3. 내가 속한 동아리 목록 조회
    print("\n3️⃣ 내가 속한 동아리 목록 조회...")
    clubs_response = requests.get(MY_CLUBS_URL, cookies=cookies)
    print(f"🔍 [TEST] 동아리 목록 응답: {clubs_response.status_code}")

    if clubs_response.status_code == 200:
        clubs_data = clubs_response.json()
        print(f"🔍 [TEST] 동아리 목록:")
        print(json.dumps(clubs_data, indent=2, ensure_ascii=False))

        # 동아리 목록에서 HeXA 동아리 찾기
        hexa_club = None
        for club in clubs_data.get("clubs", []):
            if club.get("club_name") == "HeXA":
                hexa_club = club
                break

        if hexa_club:
            print(f"🔍 [TEST] HeXA 동아리 발견: {hexa_club}")

            # 4. HeXA 동아리에서 권한 확인
            print(f"\n4️⃣ HeXA 동아리에서 권한 확인...")
            club_id = hexa_club["club_id"]

            # 4-1. 일반 권한 확인 (멤버십만 확인)
            print(f"4-1️⃣ 일반 권한 확인 (멤버십)...")
            permission_url = PERMISSION_URL.format(club_id=club_id)
            permission_response = requests.get(permission_url, cookies=cookies)
            print(f"🔍 [TEST] 일반 권한 응답: {permission_response.status_code}")

            if permission_response.status_code == 200:
                permission_data = permission_response.json()
                print(f"🔍 [TEST] 일반 권한 정보:")
                print(json.dumps(permission_data, indent=2, ensure_ascii=False))

            # 4-2. 회장 권한 확인
            print(f"\n4-2️⃣ 회장 권한 확인...")
            president_response = requests.get(
                f"{permission_url}?required_role=president", cookies=cookies
            )
            print(f"🔍 [TEST] 회장 권한 응답: {president_response.status_code}")

            if president_response.status_code == 200:
                president_data = president_response.json()
                print(f"🔍 [TEST] 회장 권한 정보:")
                print(json.dumps(president_data, indent=2, ensure_ascii=False))

            # 4-3. 일반 사용자 권한 확인 (실패해야 함)
            print(f"\n4-3️⃣ 일반 사용자 권한 확인 (실패 예상)...")
            normal_response = requests.get(
                f"{permission_url}?required_role=normal", cookies=cookies
            )
            print(f"🔍 [TEST] 일반 사용자 권한 응답: {normal_response.status_code}")

            if normal_response.status_code == 200:
                normal_data = normal_response.json()
                print(f"🔍 [TEST] 일반 사용자 권한 정보:")
                print(json.dumps(normal_data, indent=2, ensure_ascii=False))

        else:
            print("❌ [TEST] HeXA 동아리를 찾을 수 없습니다")

    # 5. 존재하지 않는 동아리에서 권한 확인 (실패 테스트)
    print(f"\n5️⃣ 존재하지 않는 동아리에서 권한 확인 (실패 테스트)...")
    fake_permission_url = PERMISSION_URL.format(club_id=99999)
    fake_response = requests.get(fake_permission_url, cookies=cookies)
    print(f"🔍 [TEST] 존재하지 않는 동아리 권한 응답: {fake_response.status_code}")

    if fake_response.status_code == 200:
        fake_data = fake_response.json()
        print(f"🔍 [TEST] 존재하지 않는 동아리 권한 정보:")
        print(json.dumps(fake_data, indent=2, ensure_ascii=False))

    # 6. 로그아웃 후 권한 확인 (실패 테스트)
    print(f"\n6️⃣ 로그아웃 후 권한 확인 (실패 테스트)...")
    logout_response = requests.post(LOGOUT_URL, cookies=cookies)
    print(f"🔍 [TEST] 로그아웃 응답: {logout_response.status_code}")

    # 로그아웃 후 권한 확인
    after_logout_response = requests.get(MY_CLUBS_URL, cookies=cookies)
    print(
        f"🔍 [TEST] 로그아웃 후 동아리 목록 응답: {after_logout_response.status_code}"
    )

    if after_logout_response.status_code == 200:
        after_logout_data = after_logout_response.json()
        print(f"🔍 [TEST] 로그아웃 후 동아리 목록:")
        print(json.dumps(after_logout_data, indent=2, ensure_ascii=False))

    print("\n🔍 [TEST] === 권한 디버깅 테스트 완료 ===")


def test_different_users():
    """다른 사용자로 권한 테스트"""
    print("\n🔍 [TEST] === 다른 사용자 권한 테스트 ===")

    # xxx 사용자로 로그인 (일반 사용자)
    print("\n1️⃣ xxx 사용자 로그인 (일반 사용자)...")
    login_data = {"email": "abcde@unist.ac.kr", "password": "password123"}

    response = requests.post(LOGIN_URL, json=login_data)
    print(f"🔍 [TEST] xxx 로그인 응답: {response.status_code}")

    if response.status_code == 200:
        cookies = response.cookies

        # 내 동아리 목록 조회
        clubs_response = requests.get(MY_CLUBS_URL, cookies=cookies)
        print(f"🔍 [TEST] xxx 동아리 목록 응답: {clubs_response.status_code}")

        if clubs_response.status_code == 200:
            clubs_data = clubs_response.json()
            print(f"🔍 [TEST] xxx 동아리 목록:")
            print(json.dumps(clubs_data, indent=2, ensure_ascii=False))

            # HeXA 동아리에서 권한 확인
            for club in clubs_data.get("clubs", []):
                if club.get("club_name") == "HeXA":
                    club_id = club["club_id"]

                    # 일반 권한 확인
                    permission_url = PERMISSION_URL.format(club_id=club_id)
                    permission_response = requests.get(permission_url, cookies=cookies)

                    if permission_response.status_code == 200:
                        permission_data = permission_response.json()
                        print(f"🔍 [TEST] xxx의 HeXA 권한:")
                        print(json.dumps(permission_data, indent=2, ensure_ascii=False))

                    # 회장 권한 확인 (실패해야 함)
                    president_response = requests.get(
                        f"{permission_url}?required_role=president", cookies=cookies
                    )

                    if president_response.status_code == 200:
                        president_data = president_response.json()
                        print(f"🔍 [TEST] xxx의 회장 권한 확인:")
                        print(json.dumps(president_data, indent=2, ensure_ascii=False))

                    break

    print("🔍 [TEST] === 다른 사용자 권한 테스트 완료 ===")


if __name__ == "__main__":
    print("🚀 권한 디버깅 테스트 시작")
    print("📝 이 테스트는 다음을 확인합니다:")
    print("  1. 로그인 후 세션 기반 권한 확인")
    print("  2. 동아리별 권한 확인")
    print("  3. 역할별 권한 확인 (president vs normal)")
    print("  4. 로그아웃 후 권한 차단")
    print("  5. 다른 사용자의 권한 차이")
    print()

    # 서버가 실행 중인지 확인
    try:
        health_check = requests.get(f"{BASE_URL}/api/v1/clubs")
        if health_check.status_code == 200:
            print("✅ 서버가 실행 중입니다")
        else:
            print("⚠️ 서버가 실행 중이지만 응답이 예상과 다릅니다")
    except:
        print("❌ 서버가 실행되지 않았습니다. 먼저 서버를 시작해주세요.")
        print("   python app.py")
        exit(1)

    # 테스트 실행
    test_permission_flow()
    test_different_users()

    print("\n🎉 권한 테스트 완료!")
    print("📋 확인 사항:")
    print("  - abcde 사용자: HeXA 동아리 회장 권한")
    print("  - xxx 사용자: HeXA 동아리 일반 사용자 권한")
    print("  - 로그아웃 후 권한 차단")
    print("  - 세션 기반 권한 확인 정상 작동")

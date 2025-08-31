#!/usr/bin/env python3
"""
ClubU API 테스트 스크립트
Mock 데이터를 사용하는 API들을 체계적으로 테스트합니다.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/v1"


def print_test_result(test_name, response):
    """테스트 결과를 깔끔하게 출력"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")
    print(f"📊 Status Code: {response.status_code}")

    try:
        data = response.json()
        print(f"📄 Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"📄 Response Text: {response.text}")

    if response.status_code == 200:
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")


def test_club_list():
    """동아리 목록 조회 테스트"""
    response = requests.get(f"{BASE_URL}/clubs/")
    print_test_result("동아리 목록 조회 (GET /clubs/)", response)
    return response


def test_club_detail(club_id=1):
    """동아리 상세 조회 테스트"""
    response = requests.get(f"{BASE_URL}/clubs/{club_id}")
    print_test_result(f"동아리 상세 조회 (GET /clubs/{club_id})", response)
    return response


def test_open_clubs():
    """모집 중인 동아리 조회 테스트"""
    response = requests.get(f"{BASE_URL}/clubs/imminent")
    print_test_result("모집 중인 동아리 조회 (GET /clubs/imminent)", response)
    return response


def test_club_questions(club_id=1):
    """동아리 지원서 문항 조회 테스트"""
    response = requests.get(f"{BASE_URL}/clubs/{club_id}/application/questions")
    print_test_result(
        f"동아리 지원서 문항 조회 (GET /clubs/{club_id}/application/questions)", response
    )
    return response


def test_add_question(club_id=1):
    """지원서 문항 추가 테스트"""
    data = {"question_text": "동아리 활동에 대한 기대사항을 알려주세요."}
    response = requests.post(
        f"{BASE_URL}/clubs/{club_id}/application/questions",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    print_test_result(
        f"지원서 문항 추가 (POST /clubs/{club_id}/application/questions)", response
    )
    return response


def test_swagger_docs():
    """Swagger 문서 접근 테스트"""
    response = requests.get("http://localhost:5000/docs/")
    print_test_result("Swagger 문서 접근 (GET /docs/)", response)
    return response


def main():
    """메인 테스트 실행"""
    print(f"\n🚀 ClubU API 테스트 시작")
    print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")

    tests = [
        (
            "기본 API 테스트",
            [
                test_club_list,
                test_club_detail,
                test_open_clubs,
                test_club_questions,
            ],
        ),
        (
            "POST API 테스트",
            [
                test_add_question,
            ],
        ),
        (
            "기타",
            [
                test_swagger_docs,
            ],
        ),
    ]

    success_count = 0
    total_count = 0

    for category, test_functions in tests:
        print(f"\n\n📂 {category}")
        print("=" * 80)

        for test_func in test_functions:
            try:
                response = test_func()
                total_count += 1
                if response.status_code in [200, 201]:
                    success_count += 1
            except Exception as e:
                print(f"❌ 테스트 실행 중 오류: {e}")
                total_count += 1

    # 테스트 결과 요약
    print(f"\n\n{'='*80}")
    print(f"📊 테스트 결과 요약")
    print(f"{'='*80}")
    print(f"✅ 성공: {success_count}/{total_count}")
    print(f"❌ 실패: {total_count - success_count}/{total_count}")
    print(f"📈 성공률: {(success_count/total_count*100):.1f}%")
    print(f"⏰ 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()

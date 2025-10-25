#!/usr/bin/env python3
"""
동아리 방 신청 API 테스트 스크립트
api.clubu.co.kr에서 새로 구현된 API들을 테스트하고 목업 데이터를 생성합니다.
"""

import requests
import json
import time
from datetime import datetime, date, timedelta
from typing import Dict, List

# API 기본 설정
BASE_URL = "https://api.clubu.co.kr/api/v1"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# 테스트용 세션 (실제로는 로그인 후 세션 쿠키를 사용해야 함)
SESSION = requests.Session()


def log_response(method: str, url: str, response: requests.Response):
    """API 응답 로깅"""
    print(f"\n{'='*60}")
    print(f"{method} {url}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}")


def test_rooms_api():
    """전체 공간 조회 API 테스트"""
    print("\n🏢 전체 공간 조회 테스트")
    url = f"{BASE_URL}/rooms"
    response = SESSION.get(url, headers=HEADERS)
    log_response("GET", url, response)
    return response.json() if response.status_code == 200 else None


def test_room_availability(room_id: int, target_date: str):
    """공간별 가용시간 조회 API 테스트"""
    print(f"\n📅 공간 {room_id} 가용시간 조회 테스트 ({target_date})")
    url = f"{BASE_URL}/rooms/{room_id}/availability"
    params = {"date": target_date}
    response = SESSION.get(url, headers=HEADERS, params=params)
    log_response("GET", url, response)
    return response.json() if response.status_code == 200 else None


def test_club_remaining_usage(club_id: int, target_date: str):
    """동아리별 사용 가능 시간 조회 API 테스트"""
    print(f"\n⏰ 동아리 {club_id} 사용 가능 시간 조회 테스트 ({target_date})")
    url = f"{BASE_URL}/rooms/clubs/{club_id}/remaining-usage"
    params = {"date": target_date}
    response = SESSION.get(url, headers=HEADERS, params=params)
    log_response("GET", url, response)
    return response.json() if response.status_code == 200 else None


def create_mock_reservation(
    club_id: int,
    user_id: int,
    room_id: int,
    target_date: str,
    start_time: str,
    end_time: str,
    note: str = None,
):
    """대관 신청 API 테스트"""
    print(f"\n📝 대관 신청 테스트")
    url = f"{BASE_URL}/reservations"
    data = {
        "club_id": club_id,
        "user_id": user_id,
        "room_id": room_id,
        "date": target_date,
        "start_time": start_time,
        "end_time": end_time,
        "note": note,
    }
    response = SESSION.post(url, headers=HEADERS, json=data)
    log_response("POST", url, response)
    return response.json() if response.status_code == 201 else None


def get_user_reservations(user_id: int, mine: bool = True, status: str = None):
    """사용자 예약 목록 조회 API 테스트"""
    print(f"\n📋 사용자 {user_id} 예약 목록 조회 테스트")
    url = f"{BASE_URL}/reservations"
    params = {"user_id": user_id, "mine": str(mine).lower()}
    if status:
        params["status"] = status

    response = SESSION.get(url, headers=HEADERS, params=params)
    log_response("GET", url, response)
    return response.json() if response.status_code == 200 else None


def get_reservation_detail(reservation_id: int):
    """예약 상세 조회 API 테스트"""
    print(f"\n🔍 예약 {reservation_id} 상세 조회 테스트")
    url = f"{BASE_URL}/reservations/{reservation_id}"
    response = SESSION.get(url, headers=HEADERS)
    log_response("GET", url, response)
    return response.json() if response.status_code == 200 else None


def cancel_reservation(reservation_id: int, user_id: int):
    """예약 취소 API 테스트"""
    print(f"\n❌ 예약 {reservation_id} 취소 테스트")
    url = f"{BASE_URL}/reservations/{reservation_id}"
    params = {"user_id": user_id}
    response = SESSION.delete(url, headers=HEADERS, params=params)
    log_response("DELETE", url, response)
    return response.json() if response.status_code == 200 else None


def create_mock_data():
    """목업 데이터 생성"""
    print("🚀 동아리 방 신청 API 목업 데이터 생성 시작")
    print("=" * 80)

    # 오늘 날짜와 내일 날짜
    today = date.today()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # 테스트용 데이터
    test_club_id = 9000  # 구름톤 유니브
    test_user_id = 9027  # groomPresident
    test_room_id = 1  # 첫 번째 공간 (실제로는 존재하는 room_id 사용)

    try:
        # 1. 전체 공간 조회
        rooms_data = test_rooms_api()
        if rooms_data and rooms_data.get("data"):
            available_rooms = rooms_data["data"]
            if available_rooms:
                test_room_id = available_rooms[0]["id"]
                print(f"✅ 사용할 공간 ID: {test_room_id}")
            else:
                print("❌ 사용 가능한 공간이 없습니다.")
                return

        # 2. 공간 가용시간 조회
        availability_data = test_room_availability(test_room_id, tomorrow_str)

        # 3. 동아리 사용 가능 시간 조회
        usage_data = test_club_remaining_usage(test_club_id, tomorrow_str)

        # 4. 대관 신청들 생성
        reservations = []

        # 첫 번째 예약: 오전 10:00-12:00
        reservation1 = create_mock_reservation(
            club_id=test_club_id,
            user_id=test_user_id,
            room_id=test_room_id,
            target_date=tomorrow_str,
            start_time="10:00",
            end_time="12:00",
            note="구름톤 유니브 정기 모임",
        )
        if reservation1:
            reservations.append(reservation1["data"])

        time.sleep(1)  # API 호출 간격 조절

        # 두 번째 예약: 오후 14:00-16:00
        reservation2 = create_mock_reservation(
            club_id=test_club_id,
            user_id=test_user_id,
            room_id=test_room_id,
            target_date=tomorrow_str,
            start_time="14:00",
            end_time="16:00",
            note="프로젝트 개발 세션",
        )
        if reservation2:
            reservations.append(reservation2["data"])

        time.sleep(1)

        # 세 번째 예약: 오후 18:00-20:00
        reservation3 = create_mock_reservation(
            club_id=test_club_id,
            user_id=test_user_id,
            room_id=test_room_id,
            target_date=tomorrow_str,
            start_time="18:00",
            end_time="20:00",
            note="코딩 테스트 준비",
        )
        if reservation3:
            reservations.append(reservation3["data"])

        # 5. 사용자 예약 목록 조회
        time.sleep(1)
        user_reservations = get_user_reservations(test_user_id, mine=True)

        # 6. 예약 상세 조회 (첫 번째 예약)
        if reservations:
            time.sleep(1)
            first_reservation_id = reservations[0]["id"]
            reservation_detail = get_reservation_detail(first_reservation_id)

        # 7. 예약 취소 테스트 (마지막 예약)
        if len(reservations) > 2:
            time.sleep(1)
            last_reservation_id = reservations[-1]["id"]
            cancel_result = cancel_reservation(last_reservation_id, test_user_id)

        print("\n🎉 목업 데이터 생성 완료!")
        print(f"📊 생성된 예약 수: {len(reservations)}")
        print(f"📅 대상 날짜: {tomorrow_str}")
        print(f"🏢 사용된 공간 ID: {test_room_id}")
        print(f"👥 동아리 ID: {test_club_id}")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback

        traceback.print_exc()


def test_api_health():
    """API 서버 상태 확인"""
    print("🏥 API 서버 상태 확인")
    try:
        # API 엔드포인트 직접 테스트
        response = SESSION.get(f"{BASE_URL}/rooms", timeout=10)
        print(f"서버 응답: {response.status_code}")
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            print("⚠️ 인증이 필요합니다. (정상적인 응답)")
            return True
        else:
            print(f"⚠️ 예상과 다른 응답: {response.status_code}")
            return True  # 일단 진행
    except Exception as e:
        print(f"❌ 서버 연결 실패: {str(e)}")
        return False


if __name__ == "__main__":
    print("🔧 동아리 방 신청 API 테스트 스크립트")
    print("=" * 80)

    # API 서버 상태 확인
    if not test_api_health():
        print("❌ API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
        exit(1)

    # 목업 데이터 생성
    create_mock_data()

    print("\n✨ 테스트 완료!")
    print("💡 실제 사용 시에는 올바른 인증 토큰이나 세션 쿠키를 설정해주세요.")

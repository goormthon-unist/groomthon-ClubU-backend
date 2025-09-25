#!/usr/bin/env python3
"""
동아리 정보 수정 API 테스트 스크립트
"""

import requests
import json
import os
from io import BytesIO
from PIL import Image

# 테스트 설정
BASE_URL = "http://localhost:5000"
CLUB_ID = 1003  # HeXA 동아리 ID
TEST_IMAGE_PATH = "test_image.png"

def create_test_image():
    """테스트용 이미지 생성"""
    # 간단한 테스트 이미지 생성
    img = Image.new('RGB', (100, 100), color='red')
    img.save(TEST_IMAGE_PATH)
    print(f"테스트 이미지 생성: {TEST_IMAGE_PATH}")

def test_club_introduction_update():
    """동아리 소개글 업데이트 테스트"""
    print("\n=== 동아리 소개글 업데이트 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/introduction"
    headers = {
        "Content-Type": "application/json",
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    data = {
        "introduction": "테스트용 동아리 소개글입니다. HeXA는 유니스트를 대표하는 IT 동아리입니다."
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_club_introduction_delete():
    """동아리 소개글 삭제 테스트"""
    print("\n=== 동아리 소개글 삭제 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/introduction"
    headers = {
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    
    try:
        response = requests.delete(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_club_logo_upload():
    """동아리 로고 업로드 테스트"""
    print("\n=== 동아리 로고 업로드 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/images/logo"
    headers = {
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'image': f}
            response = requests.put(url, headers=headers, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_club_logo_delete():
    """동아리 로고 삭제 테스트"""
    print("\n=== 동아리 로고 삭제 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/images/logo"
    headers = {
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    
    try:
        response = requests.delete(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_club_introduction_image_upload():
    """동아리 소개글 이미지 업로드 테스트"""
    print("\n=== 동아리 소개글 이미지 업로드 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/images/introduction"
    headers = {
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'image': f}
            response = requests.put(url, headers=headers, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_club_introduction_image_delete():
    """동아리 소개글 이미지 삭제 테스트"""
    print("\n=== 동아리 소개글 이미지 삭제 테스트 ===")
    
    url = f"{BASE_URL}/api/v1/clubs/{CLUB_ID}/images/introduction"
    headers = {
        "Cookie": "session_id=test-session"  # 실제 세션 ID로 교체 필요
    }
    
    try:
        response = requests.delete(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def cleanup():
    """테스트 파일 정리"""
    if os.path.exists(TEST_IMAGE_PATH):
        os.remove(TEST_IMAGE_PATH)
        print(f"테스트 이미지 삭제: {TEST_IMAGE_PATH}")

def main():
    """메인 테스트 함수"""
    print("동아리 정보 수정 API 테스트 시작")
    print("=" * 50)
    
    # 테스트 이미지 생성
    create_test_image()
    
    # 테스트 실행
    tests = [
        ("동아리 소개글 업데이트", test_club_introduction_update),
        ("동아리 소개글 삭제", test_club_introduction_delete),
        ("동아리 로고 업로드", test_club_logo_upload),
        ("동아리 로고 삭제", test_club_logo_delete),
        ("동아리 소개글 이미지 업로드", test_club_introduction_image_upload),
        ("동아리 소개글 이미지 삭제", test_club_introduction_image_delete),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"결과: {'성공' if result else '실패'}")
        except Exception as e:
            print(f"테스트 실행 중 오류: {e}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "="*50)
    print("테스트 결과 요약:")
    print("="*50)
    
    success_count = 0
    for test_name, result in results:
        status = "성공" if result else "실패"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n총 {len(results)}개 테스트 중 {success_count}개 성공")
    
    # 정리
    cleanup()

if __name__ == "__main__":
    main()

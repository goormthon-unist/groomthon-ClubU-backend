#!/usr/bin/env python3
"""
Black 포맷팅 자동화 스크립트
사용법: python format.py
"""
import subprocess
import sys


def run_black():
    """Black 포맷팅 실행"""
    try:
        print("🎨 Black 포맷팅 실행 중...")
        result = subprocess.run(["black", "."], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Black 포맷팅 완료!")
            print(result.stdout)
        else:
            print("❌ Black 포맷팅 실패:")
            print(result.stderr)
            return False

        return True
    except FileNotFoundError:
        print("❌ Black이 설치되지 않았습니다. pip install black으로 설치하세요.")
        return False


def check_git_status():
    """Git 상태 확인"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        if result.stdout.strip():
            print("📝 변경된 파일들:")
            print(result.stdout)
            return True
        else:
            print("✅ 변경사항 없음")
            return False
    except FileNotFoundError:
        print("❌ Git이 설치되지 않았습니다.")
        return False


if __name__ == "__main__":
    print("🚀 자동 포맷팅 시작...")

    if run_black():
        if check_git_status():
            print(
                "💡 팁: 'git add . && git commit -m \"style: Apply black formatting\"'로 커밋하세요!"
            )
        print("🎉 완료!")
    else:
        sys.exit(1)

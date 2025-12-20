"""
타임존 유틸리티 함수
KST(Asia/Seoul) 시간을 반환하는 함수 제공
"""

from datetime import datetime
import pytz


def get_kst_now():
    """현재 KST(Asia/Seoul) 시간을 반환"""
    kst = pytz.timezone("Asia/Seoul")
    return datetime.now(kst)


def get_kst_utcnow():
    """
    KST 시간을 반환 (datetime.utcnow() 대체용)
    모델의 default 함수로 사용하기 위해 호출 가능한 함수 반환
    """
    kst = pytz.timezone("Asia/Seoul")
    return datetime.now(kst)

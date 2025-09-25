"""
공지사항 첨부파일 관련 Mock 서비스
데이터베이스 없이 API 테스트를 위한 서비스
"""

from datetime import datetime
import uuid

# Mock 공지사항 첨부파일 데이터
MOCK_NOTICE_ASSETS = {
    1: [  # notice_id = 1
        {
            "id": 1,
            "notice_id": 1,
            "asset_type": "IMAGE",
            "file_url": "/notices/1/images/sample_image.webp",
            "created_at": "2024-09-25T10:00:00",
        },
        {
            "id": 2,
            "notice_id": 1,
            "asset_type": "FILE",
            "file_url": "/notices/1/files/sample_document.pdf",
            "created_at": "2024-09-25T10:05:00",
        },
    ],
    2: [  # notice_id = 2
        {
            "id": 3,
            "notice_id": 2,
            "asset_type": "IMAGE",
            "file_url": "/notices/2/images/another_image.webp",
            "created_at": "2024-09-25T11:00:00",
        }
    ],
}

# Mock 공지사항 데이터
MOCK_NOTICES = {
    1: {
        "id": 1,
        "club_id": 1,
        "user_id": 101,
        "title": "테스트 공지사항 1",
        "content": "이것은 테스트 공지사항입니다.",
        "status": "POSTED",
        "is_important": False,
        "views": 10,
        "posted_at": "2024-09-25T09:00:00",
    },
    2: {
        "id": 2,
        "club_id": 1,
        "user_id": 101,
        "title": "테스트 공지사항 2",
        "content": "또 다른 테스트 공지사항입니다.",
        "status": "POSTED",
        "is_important": True,
        "views": 5,
        "posted_at": "2024-09-25T10:00:00",
    },
}


def create_notice_asset(notice_id, asset_type, file):
    """공지사항 첨부파일 생성 (Mock)"""
    try:
        # 공지사항 존재 확인
        if notice_id not in MOCK_NOTICES:
            raise ValueError("존재하지 않는 공지사항입니다")

        # 파일 타입 검증
        if asset_type not in ["IMAGE", "FILE"]:
            raise ValueError("유효하지 않은 첨부파일 타입입니다")

        # Mock 파일 저장 (실제로는 파일을 저장하지 않음)
        file_extension = "webp" if asset_type == "IMAGE" else "pdf"
        mock_filename = f"{uuid.uuid4()}.{file_extension}"
        mock_file_path = f"/notices/{notice_id}/{'images' if asset_type == 'IMAGE' else 'files'}/{mock_filename}"

        # Mock 데이터 생성
        new_asset = {
            "id": len(MOCK_NOTICE_ASSETS.get(notice_id, [])) + 1,
            "notice_id": notice_id,
            "asset_type": asset_type,
            "file_url": mock_file_path,
            "created_at": datetime.now().isoformat(),
        }

        # Mock 데이터에 추가
        if notice_id not in MOCK_NOTICE_ASSETS:
            MOCK_NOTICE_ASSETS[notice_id] = []
        MOCK_NOTICE_ASSETS[notice_id].append(new_asset)

        return new_asset

    except Exception as e:
        raise Exception(f"첨부파일 생성 중 오류 발생: {e}")


def get_notice_assets(notice_id):
    """공지사항의 모든 첨부파일 조회 (Mock)"""
    try:
        return MOCK_NOTICE_ASSETS.get(notice_id, [])

    except Exception as e:
        raise Exception(f"첨부파일 조회 중 오류 발생: {e}")


def delete_notice_asset_by_id(asset_id):
    """공지사항 첨부파일 삭제 (Mock)"""
    try:
        # 모든 공지사항에서 해당 asset_id 찾아서 삭제
        for notice_id, assets in MOCK_NOTICE_ASSETS.items():
            for i, asset in enumerate(assets):
                if asset["id"] == asset_id:
                    del MOCK_NOTICE_ASSETS[notice_id][i]
                    return True

        raise ValueError("존재하지 않는 첨부파일입니다")

    except Exception as e:
        raise Exception(f"첨부파일 삭제 중 오류 발생: {e}")


def delete_all_notice_assets(notice_id):
    """공지사항의 모든 첨부파일 삭제 (Mock)"""
    try:
        if notice_id in MOCK_NOTICE_ASSETS:
            MOCK_NOTICE_ASSETS[notice_id] = []
            return True
        return True

    except Exception as e:
        raise Exception(f"첨부파일 일괄 삭제 중 오류 발생: {e}")


def update_notice_asset(asset_id, asset_type, file):
    """공지사항 첨부파일 수정 (Mock)"""
    try:
        # 모든 공지사항에서 해당 asset_id 찾아서 수정
        for notice_id, assets in MOCK_NOTICE_ASSETS.items():
            for asset in assets:
                if asset["id"] == asset_id:
                    # Mock 파일 저장
                    file_extension = "webp" if asset_type == "IMAGE" else "pdf"
                    mock_filename = f"{uuid.uuid4()}.{file_extension}"
                    mock_file_path = f"/notices/{notice_id}/{'images' if asset_type == 'IMAGE' else 'files'}/{mock_filename}"

                    # 데이터 업데이트
                    asset["asset_type"] = asset_type
                    asset["file_url"] = mock_file_path
                    asset["created_at"] = datetime.now().isoformat()

                    return asset

        raise ValueError("존재하지 않는 첨부파일입니다")

    except Exception as e:
        raise Exception(f"첨부파일 수정 중 오류 발생: {e}")

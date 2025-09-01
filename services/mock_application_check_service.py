"""
지원서 확인 관련 Mock 서비스
데이터베이스 없이 API 테스트를 위한 서비스
"""

from datetime import datetime

# Mock 지원자 데이터
MOCK_APPLICANTS = [
    {
        "application_id": 1,
        "user_id": 101,
        "name": "김지원",
        "student_id": "20210001",
        "email": "jiwon.kim@unist.ac.kr",
        "phone_number": "010-1234-5678",
        "gender": "FEMALE",
        "department": {
            "id": 1,
            "degree_course": "학사",
            "college": "공과대학",
            "major": "컴퓨터공학과",
        },
        "status": "SUBMITTED",
        "submitted_at": "2024-08-30T14:30:00",
        "answer_count": 2,
        "club_id": 1,
    },
    {
        "application_id": 2,
        "user_id": 102,
        "name": "박민수",
        "student_id": "20210002",
        "email": "minsu.park@unist.ac.kr",
        "phone_number": "010-2345-6789",
        "gender": "MALE",
        "department": {
            "id": 2,
            "degree_course": "학사",
            "college": "경영대학",
            "major": "경영학과",
        },
        "status": "VIEWED",
        "submitted_at": "2024-08-29T16:45:00",
        "answer_count": 2,
        "club_id": 1,
    },
    {
        "application_id": 3,
        "user_id": 103,
        "name": "이수진",
        "student_id": "20210003",
        "email": "sujin.lee@unist.ac.kr",
        "phone_number": "010-3456-7890",
        "gender": "FEMALE",
        "department": {
            "id": 3,
            "degree_course": "석사",
            "college": "디자인대학",
            "major": "디자인학과",
        },
        "status": "ACCEPTED",
        "submitted_at": "2024-08-28T10:20:00",
        "answer_count": 2,
        "club_id": 2,
    },
]

# Mock 지원서 상세 데이터
MOCK_APPLICATION_DETAILS = {
    1: {
        "application_id": 1,
        "status": "SUBMITTED",
        "submitted_at": "2024-08-30T14:30:00",
        "user": {
            "id": 101,
            "name": "김지원",
            "student_id": "20210001",
            "email": "jiwon.kim@unist.ac.kr",
            "phone_number": "010-1234-5678",
            "gender": "FEMALE",
            "department": {
                "id": 1,
                "degree_course": "학사",
                "college": "공과대학",
                "major": "컴퓨터공학과",
            },
        },
        "club": {"id": 1, "name": "UNIST 코딩클럽"},
        "answers": [
            {
                "id": 1,
                "question_id": 1,
                "question_text": "프로그래밍 경험이 있으신가요? 있다면 어떤 언어를 다룰 수 있나요?",
                "answer_order": 1,
                "answer_text": "Python과 JavaScript를 주로 사용하며, 웹 개발 프로젝트 경험이 있습니다.",
            },
            {
                "id": 2,
                "question_id": 2,
                "question_text": "동아리에서 하고 싶은 프로젝트나 활동이 있나요?",
                "answer_order": 2,
                "answer_text": "AI 기반 학습 도우미 앱을 개발해보고 싶습니다.",
            },
        ],
    },
    2: {
        "application_id": 2,
        "status": "VIEWED",
        "submitted_at": "2024-08-29T16:45:00",
        "user": {
            "id": 102,
            "name": "박민수",
            "student_id": "20210002",
            "email": "minsu.park@unist.ac.kr",
            "phone_number": "010-2345-6789",
            "gender": "MALE",
            "department": {
                "id": 2,
                "degree_course": "학사",
                "college": "경영대학",
                "major": "경영학과",
            },
        },
        "club": {"id": 1, "name": "UNIST 코딩클럽"},
        "answers": [
            {
                "id": 3,
                "question_id": 1,
                "question_text": "프로그래밍 경험이 있으신가요? 있다면 어떤 언어를 다룰 수 있나요?",
                "answer_order": 1,
                "answer_text": "Java를 기본적으로 다룰 수 있고, 최근에 React를 배우고 있습니다.",
            },
            {
                "id": 4,
                "question_id": 2,
                "question_text": "동아리에서 하고 싶은 프로젝트나 활동이 있나요?",
                "answer_order": 2,
                "answer_text": "경영과 IT를 결합한 비즈니스 솔루션을 개발하고 싶습니다.",
            },
        ],
    },
}


def get_club_applicants(club_id):
    """특정 동아리의 지원자 리스트를 조회 (Mock)"""
    try:
        # 해당 동아리의 지원자만 필터링
        applicants = [
            applicant
            for applicant in MOCK_APPLICANTS
            if applicant["club_id"] == club_id
        ]

        if not applicants:
            # 동아리 ID가 존재하는지 확인 (간단한 체크)
            if club_id not in [1, 2, 3, 4, 5]:  # Mock 동아리 ID들
                raise ValueError(f"동아리 ID {club_id}를 찾을 수 없습니다")
            return []

        return applicants

    except Exception as e:
        raise Exception(f"지원자 목록 조회 중 오류 발생: {str(e)}")


def get_application_detail(application_id):
    """특정 지원서의 상세 정보를 조회 (Mock)"""
    try:
        if application_id not in MOCK_APPLICATION_DETAILS:
            raise ValueError(f"지원서 ID {application_id}를 찾을 수 없습니다")

        return MOCK_APPLICATION_DETAILS[application_id]

    except Exception as e:
        raise Exception(f"지원서 상세 조회 중 오류 발생: {str(e)}")


def register_club_member(
    application_id, role_id=None, generation=None, other_info=None
):
    """지원자를 동아리원으로 등록 (Mock)"""
    try:
        # Mock 응답
        return {
            "message": "동아리원 등록이 완료되었습니다 (Mock)",
            "member": {
                "id": 999,
                "user_name": "김지원",
                "student_id": "20210001",
                "club_name": "UNIST 코딩클럽",
                "role_name": "일반회원",
                "generation": generation or 5,
                "joined_at": "2024-09-01T00:10:00",
            },
        }
    except Exception as e:
        raise Exception(f"동아리원 등록 중 오류 발생: {str(e)}")

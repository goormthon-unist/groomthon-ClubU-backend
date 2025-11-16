from models import db, Club, ClubCategory, ClubApplicationQuestion, ClubMember


def get_all_clubs():
    """모든 동아리 정보를 카테고리와 함께 조회"""
    try:
        # 동아리와 카테고리 정보를 함께 조회
        clubs = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .all()
        )

        if not clubs:
            raise ValueError("등록된 동아리가 없습니다")

        # JSON 변환
        return [
            {
                "id": club.id,
                "name": club.name,
                "activity_summary": club.activity_summary,
                "category": {"id": category.id, "name": category.name},
                "recruitment_status": club.recruitment_status,
                "president_name": club.president_name,
                "contact": club.contact,
                "current_generation": club.current_generation,
                "introduction": club.introduction,
                "recruitment_start": (
                    club.recruitment_start.isoformat()
                    if club.recruitment_start
                    else None
                ),
                "recruitment_finish": (
                    club.recruitment_finish.isoformat()
                    if club.recruitment_finish
                    else None
                ),
                "logo_image": club.logo_image,
                "introduction_image": club.introduction_image,
                "club_room": club.club_room,
                "created_at": (
                    club.created_at.isoformat() if club.created_at else None
                ),
                "updated_at": (
                    club.updated_at.isoformat() if club.updated_at else None
                ),
            }
            for club, category in clubs
        ]

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"동아리 목록 조회 중 오류 발생: {str(e)}")


def get_club_by_id(club_id):
    """특정 동아리의 상세 정보를 조회"""
    try:
        club_data = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Club.id == club_id)
            .first()
        )

        if not club_data:
            return None

        club, category = club_data

        # JSON 변환
        return {
            "id": club.id,
            "name": club.name,
            "activity_summary": club.activity_summary,
            "category": {"id": category.id, "name": category.name},
            "recruitment_status": club.recruitment_status,
            "president_name": club.president_name,
            "contact": club.contact,
            "current_generation": club.current_generation,
            "introduction": club.introduction,
            "recruitment_start": (
                club.recruitment_start.isoformat() if club.recruitment_start else None
            ),
            "recruitment_finish": (
                club.recruitment_finish.isoformat() if club.recruitment_finish else None
            ),
            "logo_image": club.logo_image,
            "introduction_image": club.introduction_image,
            "club_room": club.club_room,
            "created_at": (club.created_at.isoformat() if club.created_at else None),
            "updated_at": (club.updated_at.isoformat() if club.updated_at else None),
        }

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"동아리 상세 조회 중 오류 발생: {str(e)}")


def update_club_info(club_id, update_data):
    """동아리 정보 수정"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 업데이트 가능한 필드들
        allowed_fields = [
            "name",
            "activity_summary",
            "president_name",
            "contact",
            "category_id",
        ]

        for field in allowed_fields:
            if field in update_data:
                setattr(club, field, update_data[field])

        db.session.commit()
        return get_club_by_id(club_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 정보 수정 중 오류 발생: {str(e)}")


def update_club_status(club_id, status):
    """동아리 모집 상태 변경"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        if status not in ["OPEN", "CLOSED"]:
            raise ValueError("유효하지 않은 모집 상태입니다")

        club.recruitment_status = status
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        raise Exception(f"동아리 상태 변경 중 오류 발생: {str(e)}")


def get_club_questions(club_id):
    """동아리 지원서 문항 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        questions = ClubApplicationQuestion.query.filter_by(club_id=club_id).all()

        return [
            {
                "id": question.id,
                "club_id": question.club_id,
                "question_text": question.question_text,
                "order": question.question_order,
            }
            for question in questions
        ]

    except Exception as e:
        raise Exception(f"지원서 문항 조회 중 오류 발생: {str(e)}")


# 기존 개별 추가 함수 (주석처리 - deprecated)
# def add_club_question(club_id, question_data):
#     """동아리 지원서 문항 추가"""
#     try:
#         club = Club.query.get(club_id)
#         if not club:
#             raise ValueError("해당 동아리를 찾을 수 없습니다")

#         # 기존 문항들의 최대 order 값 찾기
#         max_order = (
#             db.session.query(db.func.max(ClubApplicationQuestion.question_order))
#             .filter_by(club_id=club_id)
#             .scalar()
#             or 0
#         )

#         new_question = ClubApplicationQuestion(
#             club_id=club_id,
#             question_text=question_data["question_text"],
#             question_order=max_order + 1,
#         )

#         db.session.add(new_question)
#         db.session.commit()

#         return {
#             "id": new_question.id,
#             "club_id": new_question.club_id,
#             "question_text": new_question.question_text,
#             "order": new_question.question_order,
#         }

#     except Exception as e:
#         db.session.rollback()
#         raise Exception(f"지원서 문항 추가 중 오류 발생: {str(e)}")


# 기존 개별 수정 함수 (주석처리 - deprecated)
# def update_question(question_id, update_data):
#     """지원서 문항 수정"""
#     try:
#         question = ClubApplicationQuestion.query.get(question_id)
#         if not question:
#             raise ValueError("해당 문항을 찾을 수 없습니다")

#         # 업데이트 가능한 필드들
#         allowed_fields = ["question_text"]

#         for field in allowed_fields:
#             if field in update_data:
#                 setattr(question, field, update_data[field])

#         db.session.commit()

#         return {
#             "id": question.id,
#             "club_id": question.club_id,
#             "question_text": question.question_text,
#             "order": question.question_order,
#         }

#     except Exception as e:
#         db.session.rollback()
#         raise Exception(f"문항 수정 중 오류 발생: {str(e)}")


# 기존 개별 삭제 함수 (주석처리 - deprecated)
# def delete_question(question_id):
#     """지원서 문항 삭제"""
#     try:
#         question = ClubApplicationQuestion.query.get(question_id)
#         if not question:
#             raise ValueError("해당 문항을 찾을 수 없습니다")

#         db.session.delete(question)
#         db.session.commit()

#         return {"message": "문항이 성공적으로 삭제되었습니다"}

#     except Exception as e:
#         db.session.rollback()
#         raise Exception(f"문항 삭제 중 오류 발생: {str(e)}")


def bulk_update_questions(club_id, questions_data):
    """
    동아리 지원서 문항 일괄 업데이트 (추가/수정/삭제/순서 변경)

    프론트엔드에서 id와 question_text만 보내면 됩니다.
    - id가 있으면: 수정
    - id가 없으면: 추가
    - DB에 있지만 목록에 없으면: 삭제
    - order는 배열 순서로 자동 결정됩니다.

    Args:
        club_id: 동아리 ID
        questions_data: 문항 목록 (각 항목은 id(선택), question_text(필수), order(자동) 포함)

    Returns:
        업데이트된 문항 목록
    """
    try:
        # 동아리 존재 확인
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        # 현재 DB의 문항 목록 조회
        existing_questions = ClubApplicationQuestion.query.filter_by(
            club_id=club_id
        ).all()
        existing_questions_dict = {q.id: q for q in existing_questions}

        # 프론트엔드에서 보낸 문항들을 ID로 분류
        questions_with_id = []  # id가 있는 것들 (수정)
        questions_without_id = []  # id가 없는 것들 (추가)
        frontend_question_ids = set()

        for question_data in questions_data:
            question_id = question_data.get("id")
            question_text = question_data.get("question_text")

            # 필수 필드 검증
            if not question_text:
                raise ValueError("question_text는 필수입니다")

            if question_id:
                # 기존 문항 수정
                if question_id not in existing_questions_dict:
                    raise ValueError(f"존재하지 않는 문항 ID입니다: {question_id}")
                questions_with_id.append(
                    {
                        "id": question_id,
                        "question_text": question_text,
                    }
                )
                frontend_question_ids.add(question_id)
            else:
                # 새 문항 추가
                questions_without_id.append(
                    {
                        "question_text": question_text,
                    }
                )

        # id 값 자체를 order로 사용
        questions_to_update = {}
        questions_to_create = []

        # id가 있는 문항들: id 값 = order
        for question in questions_with_id:
            question_id = question["id"]
            questions_to_update[question_id] = {
                "question_text": question["question_text"],
                "order": question_id,  # id 값 자체를 order로 사용
            }

        # id가 없는 새 문항들: 기존 id들의 최대값 다음부터 시작
        max_id = (
            max(questions_with_id, key=lambda x: x["id"])["id"]
            if questions_with_id
            else 0
        )
        current_order = max_id + 1

        for question in questions_without_id:
            questions_to_create.append(
                {
                    "question_text": question["question_text"],
                    "order": current_order,
                }
            )
            current_order += 1

        # 삭제할 문항들 (DB에 있지만 프론트엔드 목록에 없는 것들)
        questions_to_delete = [
            q_id
            for q_id in existing_questions_dict.keys()
            if q_id not in frontend_question_ids
        ]

        # 트랜잭션 시작
        try:
            # 1. 기존 문항 수정
            for question_id, update_data in questions_to_update.items():
                question = existing_questions_dict[question_id]
                question.question_text = update_data["question_text"]
                question.question_order = update_data["order"]

            # 2. 새 문항 추가
            for question_data in questions_to_create:
                new_question = ClubApplicationQuestion(
                    club_id=club_id,
                    question_text=question_data["question_text"],
                    question_order=question_data["order"],
                )
                db.session.add(new_question)

            # 3. 삭제할 문항 삭제
            for question_id in questions_to_delete:
                question = existing_questions_dict[question_id]
                db.session.delete(question)

            # 4. 커밋
            db.session.commit()

            # 5. 업데이트된 문항 목록 반환
            updated_questions = (
                ClubApplicationQuestion.query.filter_by(club_id=club_id)
                .order_by(ClubApplicationQuestion.question_order.asc())
                .all()
            )

            return {
                "status": "success",
                "club_id": club_id,
                "count": len(updated_questions),
                "questions": [
                    {
                        "id": q.id,
                        "club_id": q.club_id,
                        "question_text": q.question_text,
                        "order": q.question_order,
                    }
                    for q in updated_questions
                ],
            }

        except Exception as e:
            db.session.rollback()
            raise

    except ValueError:
        raise
    except Exception as e:
        db.session.rollback()
        raise Exception(f"지원서 문항 일괄 업데이트 중 오류 발생: {str(e)}")


def get_open_clubs():
    """모집 중인 동아리 정보를 카테고리와 함께 조회"""
    try:
        # 모집 중인 동아리와 카테고리 정보를 함께 조회
        clubs = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Club.recruitment_status == "OPEN")
            .all()
        )

        if not clubs:
            return []  # 빈 리스트 반환 (에러가 아님)

        # JSON 변환 - 요청된 형식에 맞춰 모든 필드 포함
        return [
            {
                "id": club.id,
                "name": club.name,
                "category": {"id": category.id, "name": category.name},
                "activity_summary": club.activity_summary,
                "introduction": club.introduction,
                "recruitment_status": club.recruitment_status,
                "current_generation": club.current_generation,
                "president_name": club.president_name,
                "contact": club.contact,
                "recruitment_start": (
                    club.recruitment_start.isoformat()
                    if club.recruitment_start
                    else None
                ),
                "recruitment_finish": (
                    club.recruitment_finish.isoformat()
                    if club.recruitment_finish
                    else None
                ),
                "logo_image": club.logo_image,
                "introduction_image": club.introduction_image,
                "club_room": club.club_room,
                "created_at": (
                    club.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                    if club.created_at
                    else None
                ),
                "updated_at": (
                    club.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                    if club.updated_at
                    else None
                ),
            }
            for club, category in clubs
        ]

    except Exception as e:
        # 데이터베이스 오류를 상위로 전달
        raise Exception(f"모집 중인 동아리 목록 조회 중 오류 발생: {str(e)}")


def get_club_members(club_id):
    """동아리원 목록 조회"""
    try:
        club = Club.query.get(club_id)
        if not club:
            raise ValueError("해당 동아리를 찾을 수 없습니다")

        members = ClubMember.query.filter_by(club_id=club_id).all()

        return [
            {
                "id": member.id,
                "club_id": member.club_id,
                "user_id": member.user_id,
                "role_id": member.role_id,
                "generation": member.generation,
                "other_info": member.other_info,
                "joined_at": (
                    member.joined_at.isoformat() if member.joined_at else None
                ),
            }
            for member in members
        ]

    except Exception as e:
        raise Exception(f"동아리원 목록 조회 중 오류 발생: {str(e)}")

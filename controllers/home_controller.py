from flask_restx import Resource, reqparse
from services.session_service import get_current_session
from utils.permission_decorator import require_permission
from services.home_service import (
    get_all_clubs,
    get_club_by_id,
    # update_club_info,  # 주석처리 - deprecated
    # update_club_status,  # 주석처리 - deprecated
    bulk_update_club_info,  # 새로운 통합 bulk update 함수
    # add_club_question,  # 주석처리 - deprecated
    # update_question,  # 주석처리 - deprecated
    # delete_question,  # 주석처리 - deprecated
    bulk_update_questions,  # 새로운 bulk update 함수
    get_club_members,
)


class ClubListController(Resource):
    """동아리 목록 조회 컨트롤러"""

    def get(self):
        """모든 동아리 목록을 반환합니다"""
        try:
            clubs_data = get_all_clubs()
            return {
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-01"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


class ClubUpdateController(Resource):
    """동아리 정보 조회/수정 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 상세 정보를 반환합니다"""
        try:
            club_data = get_club_by_id(club_id)
            if not club_data:
                return {
                    "status": "error",
                    "message": "해당 동아리를 찾을 수 없습니다",
                    "code": "404-01",
                }, 404

            return club_data, 200
        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-02"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

    # 기존 개별 수정 메서드 (주석처리 - deprecated)
    # def patch(self, club_id):
    #     """동아리 정보를 수정합니다"""
    #     try:
    #         # 세션 인증 확인
    #         session_data = get_current_session()
    #         if not session_data:
    #             return {
    #                 "status": "error",
    #                 "message": "로그인이 필요합니다",
    #                 "code": "401-01",
    #             }, 401

    #         parser = reqparse.RequestParser()
    #         parser.add_argument("name", type=str, location="json")
    #         parser.add_argument("activity_summary", type=str, location="json")
    #         parser.add_argument("president_name", type=str, location="json")
    #         parser.add_argument("contact", type=str, location="json")
    #         parser.add_argument("category_id", type=int, location="json")
    #         args = parser.parse_args()
    #         update_data = {k: v for k, v in args.items() if v is not None}

    #         if not update_data:
    #             return {
    #                 "status": "error",
    #                 "message": "수정할 데이터가 없습니다",
    #                 "code": "400-03",
    #             }, 400

    #         club_data = update_club_info(club_id, update_data)
    #         return club_data, 200

    #     except ValueError as e:
    #         return {"status": "error", "message": str(e), "code": "400-04"}, 400
    #     except Exception as e:
    #         return {
    #             "status": "error",
    #             "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
    #             "code": "500-00",
    #         }, 500

    # 새로운 통합 업데이트 메서드
    @require_permission("clubs.update", club_id_param="club_id")
    def put(self, club_id):
        """동아리 정보 일괄 업데이트 (통합 API)"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            # JSON 요청 본문 직접 파싱 (null 처리 명확하게)
            from flask import request

            json_data = request.get_json() or {}

            # 업데이트 가능한 필드 목록
            allowed_fields = [
                "name",
                "activity_summary",
                "president_name",
                "contact",
                "club_room",
                "recruitment_start",
                "recruitment_finish",
                "introduction",
                "recruitment_status",
            ]

            # 요청에 포함된 필드만 추출 (None도 포함하여 null 처리 가능)
            update_data = {k: v for k, v in json_data.items() if k in allowed_fields}

            # 최소 하나의 필드는 있어야 함
            if not any(v is not None for v in update_data.values()):
                return {
                    "status": "error",
                    "message": "수정할 데이터가 없습니다",
                    "code": "400-03",
                }, 400

            club_data = bulk_update_club_info(club_id, update_data)
            return club_data, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-04"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


# 기존 모집 상태 변경 컨트롤러 (주석처리 - deprecated)
# class ClubStatusController(Resource):
#     """동아리 모집 상태 변경 컨트롤러"""

#     def patch(self, club_id):
#         """동아리 모집 상태를 변경합니다"""
#         try:
#             # 세션 인증 확인
#             session_data = get_current_session()
#             if not session_data:
#                 return {
#                     "status": "error",
#                     "message": "로그인이 필요합니다",
#                     "code": "401-01",
#                 }, 401

#             parser = reqparse.RequestParser()
#             parser.add_argument("status", type=str, required=True, location="json")
#             args = parser.parse_args()
#             status = args["status"]

#             update_club_status(club_id, status)
#             return {
#                 "message": "동아리 모집 상태가 성공적으로 변경되었습니다.",
#                 "club_id": club_id,
#                 "recruitment_status": status,
#             }, 200

#         except ValueError as e:
#             return {"status": "error", "message": str(e), "code": "400-05"}, 400
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
#                 "code": "500-00",
#             }, 500


class ClubQuestionsController(Resource):
    """동아리 지원서 문항 관리 컨트롤러"""

    # 기존 개별 추가 메서드 (주석처리 - deprecated)
    # def post(self, club_id):
    #     """동아리 지원서 문항을 추가합니다"""
    #     try:
    #         # 세션 인증 확인
    #         session_data = get_current_session()
    #         if not session_data:
    #             return {
    #                 "status": "error",
    #                 "message": "로그인이 필요합니다",
    #                 "code": "401-01",
    #             }, 401

    #         parser = reqparse.RequestParser()
    #         parser.add_argument(
    #             "question_text", type=str, required=True, location="json"
    #         )
    #         args = parser.parse_args()
    #         question_data = {"question_text": args["question_text"]}

    #         new_question = add_club_question(club_id, question_data)
    #         return new_question, 201

    #     except ValueError as e:
    #         return {"status": "error", "message": str(e), "code": "400-07"}, 400
    #     except Exception as e:
    #         return {
    #             "status": "error",
    #             "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
    #             "code": "500-00",
    #         }, 500

    # 새로운 Bulk Update 메서드
    @require_permission("application_questions.update", club_id_param="club_id")
    def put(self, club_id):
        """동아리 지원서 문항을 일괄 업데이트합니다 (추가/수정/삭제/순서 변경)"""
        try:
            # 세션 인증 확인
            session_data = get_current_session()
            if not session_data:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다",
                    "code": "401-01",
                }, 401

            parser = reqparse.RequestParser()
            parser.add_argument("questions", type=list, required=True, location="json")
            args = parser.parse_args()

            if not args["questions"]:
                return {
                    "status": "error",
                    "message": "questions 배열이 필요합니다",
                    "code": "400-12",
                }, 400

            # questions 배열 검증
            questions_data = args["questions"]
            if not isinstance(questions_data, list):
                return {
                    "status": "error",
                    "message": "questions는 배열이어야 합니다",
                    "code": "400-13",
                }, 400

            # 각 문항 검증
            validated_questions = []
            for i, question in enumerate(questions_data):
                if not isinstance(question, dict):
                    return {
                        "status": "error",
                        "message": f"questions[{i}]는 객체여야 합니다",
                        "code": "400-14",
                    }, 400
                if "question_text" not in question or not question["question_text"]:
                    return {
                        "status": "error",
                        "message": f"questions[{i}]에 question_text가 필요합니다",
                        "code": "400-15",
                    }, 400

                validated_question = {
                    "id": question.get("id"),  # id는 선택사항
                    "question_text": question["question_text"],
                }
                validated_questions.append(validated_question)

            # order는 id 순서대로 자동 설정 (id가 있는 것들 먼저, 그 다음 새 것들)
            result = bulk_update_questions(club_id, validated_questions)
            return result, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-17"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500


# 기존 문항 수정/삭제 컨트롤러 (주석처리 - deprecated)
# class QuestionController(Resource):
#     """지원서 문항 수정/삭제 컨트롤러"""

#     def patch(self, question_id):
#         """지원서 문항을 수정합니다"""
#         try:
#             # 세션 인증 확인
#             session_data = get_current_session()
#             if not session_data:
#                 return {
#                     "status": "error",
#                     "message": "로그인이 필요합니다",
#                     "code": "401-01",
#                 }, 401

#             parser = reqparse.RequestParser()
#             parser.add_argument("question_text", type=str, location="json")
#             args = parser.parse_args()
#             update_data = {k: v for k, v in args.items() if v is not None}

#             if not update_data:
#                 return {
#                     "status": "error",
#                     "message": "수정할 데이터가 없습니다",
#                     "code": "400-08",
#                 }, 400

#             question_data = update_question(question_id, update_data)
#             return question_data, 200

#         except ValueError as e:
#             return {"status": "error", "message": str(e), "code": "400-09"}, 400
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
#                 "code": "500-00",
#             }, 500

#     def delete(self, question_id):
#         """지원서 문항을 삭제합니다"""
#         try:
#             # 세션 인증 확인
#             session_data = get_current_session()
#             if not session_data:
#                 return {
#                     "status": "error",
#                     "message": "로그인이 필요합니다",
#                     "code": "401-01",
#                 }, 401

#             result = delete_question(question_id)
#             return {"message": result["message"]}, 200

#         except ValueError as e:
#             return {"status": "error", "message": str(e), "code": "400-10"}, 400
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
#                 "code": "500-00",
#             }, 500


class ClubMembersController(Resource):
    """동아리원 목록 조회 컨트롤러"""

    @require_permission("clubs.members", club_id_param="club_id")
    def get(self, club_id):
        """동아리원 목록을 조회합니다"""
        try:
            members = get_club_members(club_id)
            return {
                "count": len(members),
                "members": members,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": "400-11"}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"서버 내부 오류가 발생했습니다 - {str(e)}",
                "code": "500-00",
            }, 500

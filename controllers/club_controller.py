from flask_restx import Resource, abort, fields
from services.club_service import (
    get_all_clubs, 
    get_club_by_id, 
    update_club_info, 
    update_club_status, 
    get_club_members
)
from services.application_question_service import (
    get_club_questions,
    create_club_question,
    update_club_question,
    delete_club_question
)


# API 모델 정의
def create_api_models(api):
    """API 응답 모델 정의"""
    
    # 카테고리 모델
    category_model = api.model('Category', {
        'id': fields.Integer(description='카테고리 ID'),
        'name': fields.String(description='카테고리명')
    })
    
    # 동아리 모델
    club_model = api.model('Club', {
        'id': fields.Integer(description='동아리 ID'),
        'name': fields.String(description='동아리명'),
        'activity_summary': fields.String(description='활동 요약'),
        'category': fields.Nested(category_model, description='카테고리 정보'),
        'recruitment_status': fields.String(description='모집 상태 (OPEN/CLOSED)'),
        'president_name': fields.String(description='회장명'),
        'contact': fields.String(description='연락처'),
        'created_at': fields.String(description='생성일시'),
        'updated_at': fields.String(description='수정일시')
    })
    
    # 동아리 목록 응답 모델
    club_list_response = api.model('ClubListResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'count': fields.Integer(description='동아리 개수'),
        'clubs': fields.List(fields.Nested(club_model), description='동아리 목록')
    })
    
    # 동아리 상세 응답 모델
    club_detail_response = api.model('ClubDetailResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'club': fields.Nested(club_model, description='동아리 상세 정보')
    })
    
    # 사용자 모델
    user_model = api.model('User', {
        'id': fields.Integer(description='사용자 ID'),
        'name': fields.String(description='사용자명'),
        'student_id': fields.String(description='학번')
    })
    
    # 역할 모델
    role_model = api.model('Role', {
        'id': fields.Integer(description='역할 ID'),
        'name': fields.String(description='역할명')
    })
    
    # 동아리원 모델
    member_model = api.model('Member', {
        'id': fields.Integer(description='동아리원 ID'),
        'user': fields.Nested(user_model, description='사용자 정보'),
        'role': fields.Nested(role_model, description='역할 정보'),
        'joined_at': fields.String(description='가입일시')
    })
    
    # 동아리원 목록 응답 모델
    member_list_response = api.model('MemberListResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'count': fields.Integer(description='동아리원 개수'),
        'members': fields.List(fields.Nested(member_model), description='동아리원 목록')
    })
    
    # 문항 모델
    question_model = api.model('Question', {
        'id': fields.Integer(description='문항 ID'),
        'club_id': fields.Integer(description='동아리 ID'),
        'question_text': fields.String(description='문항 내용'),
        'question_order': fields.Integer(description='문항 순서')
    })
    
    # 문항 목록 응답 모델
    question_list_response = api.model('QuestionListResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'count': fields.Integer(description='문항 개수'),
        'questions': fields.List(fields.Nested(question_model), description='문항 목록')
    })
    
    # 문항 생성/수정 응답 모델
    question_response = api.model('QuestionResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'question': fields.Nested(question_model, description='문항 정보')
    })
    
    # 삭제 응답 모델
    delete_response = api.model('DeleteResponse', {
        'status': fields.String(description='응답 상태', example='success'),
        'message': fields.String(description='삭제 완료 메시지')
    })
    
    return {
        'club_list_response': club_list_response,
        'club_detail_response': club_detail_response,
        'member_list_response': member_list_response,
        'question_list_response': question_list_response,
        'question_response': question_response,
        'delete_response': delete_response
    }


class ClubListController(Resource):
    """동아리 목록 조회 컨트롤러"""

    def get(self):
        """모든 동아리 목록을 반환합니다"""
        try:
            clubs_data = get_all_clubs()
            return {
                "status": "success",
                "count": len(clubs_data),
                "clubs": clubs_data,
            }, 200
        except ValueError as e:
            abort(400, f"400-01: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubDetailController(Resource):
    """동아리 상세 정보 조회 컨트롤러"""

    def get(self, club_id):
        """특정 동아리의 상세 정보를 반환합니다"""
        try:
            club_data = get_club_by_id(club_id)
            if not club_data:
                abort(404, "404-01: 해당 동아리를 찾을 수 없습니다")

            return {"status": "success", "club": club_data}, 200
        except ValueError as e:
            abort(400, f"400-02: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def patch(self, club_id):
        """동아리 정보를 수정합니다"""
        try:
            from flask import request
            update_data = request.get_json()
            
            if not update_data:
                abort(400, "400-03: 수정할 데이터가 없습니다")

            updated_club = update_club_info(club_id, update_data)
            return {"status": "success", "club": updated_club}, 200
        except ValueError as e:
            abort(400, f"400-04: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubStatusController(Resource):
    """동아리 모집 상태 변경 컨트롤러"""

    def patch(self, club_id):
        """동아리 모집 상태를 변경합니다"""
        try:
            from flask import request
            data = request.get_json()
            
            if not data or "status" not in data:
                abort(400, "400-05: 모집 상태 정보가 없습니다")

            updated_club = update_club_status(club_id, data["status"])
            return {"status": "success", "club": updated_club}, 200
        except ValueError as e:
            abort(400, f"400-06: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubMembersController(Resource):
    """동아리원 목록 조회 컨트롤러"""

    def get(self, club_id):
        """동아리원 목록을 조회합니다"""
        try:
            members_data = get_club_members(club_id)
            return {
                "status": "success",
                "count": len(members_data),
                "members": members_data,
            }, 200
        except ValueError as e:
            abort(400, f"400-07: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class ClubQuestionsController(Resource):
    """동아리 지원서 문항 조회/추가 컨트롤러"""

    def get(self, club_id):
        """동아리 지원서 문항을 조회합니다"""
        try:
            questions_data = get_club_questions(club_id)
            return {
                "status": "success",
                "count": len(questions_data),
                "questions": questions_data,
            }, 200
        except ValueError as e:
            abort(400, f"400-08: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def post(self, club_id):
        """동아리 지원서 문항을 추가합니다"""
        try:
            from flask import request
            question_data = request.get_json()
            
            if not question_data or "question_text" not in question_data:
                abort(400, "400-09: 문항 내용이 없습니다")

            new_question = create_club_question(club_id, question_data)
            return {"status": "success", "question": new_question}, 201
        except ValueError as e:
            abort(400, f"400-10: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")


class QuestionDetailController(Resource):
    """지원서 문항 수정/삭제 컨트롤러"""

    def patch(self, question_id):
        """지원서 문항을 수정합니다"""
        try:
            from flask import request
            update_data = request.get_json()
            
            if not update_data:
                abort(400, "400-11: 수정할 데이터가 없습니다")

            updated_question = update_club_question(question_id, update_data)
            return {"status": "success", "question": updated_question}, 200
        except ValueError as e:
            abort(400, f"400-12: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

    def delete(self, question_id):
        """지원서 문항을 삭제합니다"""
        try:
            result = delete_club_question(question_id)
            return {"status": "success", "message": result["message"]}, 200
        except ValueError as e:
            abort(400, f"400-13: {str(e)}")
        except Exception as e:
            abort(500, f"500-00: 서버 내부 오류가 발생했습니다 - {str(e)}")

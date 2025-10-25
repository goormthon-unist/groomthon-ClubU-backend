from flask import request
from flask_restx import Resource, Namespace
from services.cleaning_service import CleaningService
from services.session_service import get_session_info
from utils.permission_decorator import require_permission

cleaning_ns = Namespace("", description="청소 사진 관리 API")


@cleaning_ns.route("/reservations/<int:reservation_id>/occurrences/<int:occurrence_id>")
class UsageDetailController(Resource):
    @cleaning_ns.doc("get_usage_detail")
    @cleaning_ns.response(200, "성공")
    @cleaning_ns.response(404, "예약을 찾을 수 없음")
    @cleaning_ns.response(403, "권한 없음")
    @cleaning_ns.response(500, "서버 오류")
    @require_permission("cleaning.usage_detail")
    def get(self, reservation_id, occurrence_id):
        """사용 완료 후 상세 조회"""
        try:
            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            usage_detail = CleaningService.get_usage_detail(
                reservation_id, occurrence_id, user_id
            )
            return usage_detail, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 404
        except Exception as e:
            return {
                "status": "error",
                "message": f"사용 상세 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500


@cleaning_ns.route(
    "/reservations/<int:reservation_id>/occurrences/<int:occurrence_id>/cleaning/photos"
)
@cleaning_ns.route(
    "/reservations/<int:reservation_id>/occurrences/<int:occurrence_id>/cleaning/photos/<int:photo_id>"
)
class CleaningPhotoController(Resource):
    @cleaning_ns.doc("upload_cleaning_photo")
    @cleaning_ns.response(201, "청소 사진 업로드 성공")
    @cleaning_ns.response(400, "잘못된 요청")
    @cleaning_ns.response(403, "권한 없음")
    @cleaning_ns.response(500, "서버 오류")
    @require_permission("cleaning.photo_upload")
    def post(self, reservation_id, occurrence_id):
        """청소 사진 업로드"""
        try:
            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            # 파일과 메모 가져오기
            file = request.files.get("file")
            note = request.form.get("note")

            # 한국어 인코딩 처리
            if note:
                try:
                    # UTF-8로 디코딩 시도
                    if isinstance(note, bytes):
                        note = note.decode("utf-8")
                    elif isinstance(note, str):
                        # 이미 문자열이면 그대로 사용
                        pass
                except UnicodeDecodeError:
                    # UTF-8 디코딩 실패시 다른 인코딩 시도
                    try:
                        note = note.decode("latin-1").encode("latin-1").decode("utf-8")
                    except:
                        # 모든 시도 실패시 원본 유지
                        pass

            if not file:
                return {
                    "status": "error",
                    "message": "파일이 필요합니다.",
                }, 400

            photo = CleaningService.upload_cleaning_photo(
                reservation_id, occurrence_id, file, note, user_id
            )
            return photo, 201
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"청소 사진 업로드 중 오류가 발생했습니다: {str(e)}",
            }, 500

    @cleaning_ns.doc("delete_cleaning_photo")
    @cleaning_ns.response(200, "청소 사진 삭제 성공")
    @cleaning_ns.response(404, "청소 사진을 찾을 수 없음")
    @cleaning_ns.response(403, "권한 없음")
    @cleaning_ns.response(500, "서버 오류")
    @require_permission("cleaning.photo_delete")
    def delete(self, reservation_id, occurrence_id, photo_id=None):
        """청소 사진 삭제"""
        try:
            # 보안 검증: 세션에서 사용자 정보 가져오기
            session_info = get_session_info()
            if not session_info:
                return {
                    "status": "error",
                    "message": "로그인이 필요합니다.",
                }, 401

            user_id = session_info["user"]["user_id"]

            # photo_id가 URL 경로에 없으면 쿼리 파라미터에서 가져오기
            if photo_id is None:
                photo_id = request.args.get("photo_id", type=int)
                if not photo_id:
                    return {
                        "status": "error",
                        "message": "photo_id가 필요합니다.",
                    }, 400

            result = CleaningService.delete_cleaning_photo(
                reservation_id, occurrence_id, photo_id, user_id
            )
            return result, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 404
        except Exception as e:
            return {
                "status": "error",
                "message": f"청소 사진 삭제 중 오류가 발생했습니다: {str(e)}",
            }, 500


@cleaning_ns.route(
    "/admin/cleaning-submissions/<int:reservation_id>/occurrences/<int:occurrence_id>"
)
@cleaning_ns.route(
    "/admin/cleaning-submissions/<int:reservation_id>/occurrences/<int:occurrence_id>/approve"
)
@cleaning_ns.route(
    "/admin/cleaning-submissions/<int:reservation_id>/occurrences/<int:occurrence_id>/reject"
)
class AdminCleaningSubmissionController(Resource):
    @cleaning_ns.doc("get_cleaning_submission_detail")
    @cleaning_ns.response(200, "성공")
    @cleaning_ns.response(404, "예약을 찾을 수 없음")
    @cleaning_ns.response(500, "서버 오류")
    @require_permission("admin.cleaning_submissions")
    def get(self, reservation_id, occurrence_id):
        """청소 사진 제출 상세 조회 (관리자용)"""
        try:
            submission_detail = CleaningService.get_cleaning_submission_detail(
                reservation_id, occurrence_id
            )
            return submission_detail, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 404
        except Exception as e:
            return {
                "status": "error",
                "message": f"청소 사진 제출 상세 조회 중 오류가 발생했습니다: {str(e)}",
            }, 500

    @cleaning_ns.doc("approve_cleaning_submission")
    @cleaning_ns.response(200, "청소 사진 승인/반려 성공")
    @cleaning_ns.response(400, "잘못된 요청")
    @cleaning_ns.response(404, "예약을 찾을 수 없음")
    @cleaning_ns.response(500, "서버 오류")
    @require_permission("admin.cleaning_submissions")
    def post(self, reservation_id, occurrence_id):
        """청소 사진 제출 승인/반려"""
        try:
            # URL 경로에서 action 확인
            current_path = request.path
            if "/approve" in current_path:
                action = "approve"
            elif "/reject" in current_path:
                action = "reject"
            else:
                # 기존 방식: JSON body에서 action 가져오기
                try:
                    data = request.get_json() or {}
                except:
                    data = {}
                action = data.get("action")
                if not action or action not in ["approve", "reject"]:
                    return {
                        "status": "error",
                        "message": "action은 'approve' 또는 'reject'여야 합니다.",
                    }, 400

            # admin_note 안전하게 가져오기
            try:
                data = request.get_json() or {}
                admin_note = data.get("admin_note")
            except:
                admin_note = None

            result = CleaningService.approve_cleaning_submission(
                reservation_id, occurrence_id, action, admin_note
            )
            return result, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"청소 사진 승인/반려 중 오류가 발생했습니다: {str(e)}",
            }, 500

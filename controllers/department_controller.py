from flask import current_app
from flask_restx import Resource
from models import Department
from services.department_service import get_all_departments


class DepartmentListController(Resource):
    """학과 목록 조회 컨트롤러"""

    def get(self):
        """모든 학과 목록 조회 API"""
        try:
            departments = get_all_departments()
            
            return {
                "status": "success",
                "message": "학과 목록을 성공적으로 조회했습니다.",
                "data": {
                    "departments": departments,
                    "count": len(departments)
                }
            }, 200

        except Exception as e:
            current_app.logger.exception("department.list failed")
            return {
                "status": "error",
                "message": f"학과 목록 조회 중 오류가 발생했습니다: {str(e)}"
            }, 500

from flask_restx import Namespace
from controllers.department_controller import DepartmentListController

# 네임스페이스 등록
department_ns = Namespace("departments", description="학과 관리 API")


# API 엔드포인트 등록
@department_ns.route("")
class DepartmentListResource(DepartmentListController):
    """학과 목록 리소스"""

    def get(self):
        return {
            "status": "error",
            "message": "비활성화된 API입니다",
            "code": "404-00",
        }, 404

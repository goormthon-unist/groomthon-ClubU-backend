from models import db, Department


def get_all_departments():
    """모든 학과 목록 조회"""
    try:
        departments = Department.query.all()

        result = []
        for dept in departments:
            result.append(
                {
                    "id": dept.id,
                    "degree_course": dept.degree_course,
                    "college": dept.college,
                    "major": dept.major,
                }
            )

        return result

    except Exception as e:
        raise Exception(f"학과 목록 조회 중 오류 발생: {str(e)}")


def get_department_by_id(department_id):
    """특정 학과 정보 조회"""
    try:
        department = Department.query.filter_by(id=department_id).first()

        if not department:
            return None

        return {
            "id": department.id,
            "degree_course": department.degree_course,
            "college": department.college,
            "major": department.major,
        }

    except Exception as e:
        raise Exception(f"학과 정보 조회 중 오류 발생: {str(e)}")

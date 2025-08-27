from flask import Blueprint, jsonify
from models import db, Club, ClubCategory

club_bp = Blueprint("club", __name__)


@club_bp.route("/")
def get_clubs():
    """동아리 전체 목록 조회"""
    try:
        # 동아리와 카테고리 정보를 함께 조회
        clubs = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .all()
        )

        club_list = []
        for club, category in clubs:
            club_data = {
                "id": club.id,
                "name": club.name,
                "activity_summary": club.activity_summary,
                "category": {"id": category.id, "name": category.name},
                "recruitment_status": club.recruitment_status,
                "created_at": club.created_at.isoformat() if club.created_at else None,
                "updated_at": club.updated_at.isoformat() if club.updated_at else None,
            }
            club_list.append(club_data)

        return jsonify(
            {"status": "success", "count": len(club_list), "clubs": club_list}
        )

    except Exception as e:
        return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500


@club_bp.route("/<int:club_id>")
def get_club_detail(club_id):
    """특정 동아리 상세 정보 조회"""
    try:
        club = (
            db.session.query(Club, ClubCategory)
            .join(ClubCategory, Club.category_id == ClubCategory.id)
            .filter(Club.id == club_id)
            .first()
        )

        if not club:
            return jsonify({"status": "error", "message": "Club not found"}), 404

        club_obj, category = club
        club_data = {
            "id": club_obj.id,
            "name": club_obj.name,
            "activity_summary": club_obj.activity_summary,
            "category": {"id": category.id, "name": category.name},
            "recruitment_status": club_obj.recruitment_status,
            "president_name": club_obj.president_name,
            "contact": club_obj.contact,
            "created_at": club_obj.created_at.isoformat()
            if club_obj.created_at
            else None,
            "updated_at": club_obj.updated_at.isoformat()
            if club_obj.updated_at
            else None,
        }

        return jsonify({"status": "success", "club": club_data})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

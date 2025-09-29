from datetime import datetime

from . import db


class NoticeAsset(db.Model):
    __tablename__ = "notice_assets"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    notices_id = db.Column(
        db.BigInteger, db.ForeignKey("notices.id", ondelete="CASCADE"), nullable=False
    )
    asset_type = db.Column(db.Enum("IMAGE", "FILE", name="asset_type"), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=True)  # 원본 파일명 저장
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 관계 설정
    notice = db.relationship("Notice", backref="assets")

    def __repr__(self):
        return (
            f"<NoticeAsset {self.id}: {self.asset_type} for Notice {self.notices_id}>"
        )

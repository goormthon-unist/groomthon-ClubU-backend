from . import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)  # name을 role_name으로 변경

    def __repr__(self):
        return f"<Role {self.role_name}>"

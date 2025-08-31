from . import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    degree_course = db.Column(db.String(50), nullable=False)  # 학사/석사/박사
    college = db.Column(db.String(100), nullable=False)       # 단과대학
    major = db.Column(db.String(100), nullable=False)         # 전공

    def __repr__(self):
        return f"<Department {self.college} {self.major}>"

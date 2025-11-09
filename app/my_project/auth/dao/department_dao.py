from app.my_project.auth.domain.department import Department
from app.db import db

class DepartmentDAO:
    def __init__(self):
        pass

    def get_all_departments(self):
        return Department.query.all()

    def get_department_by_id(self, department_id: int):
        return Department.query.get(department_id)

    def add_department(self, department: Department):
        try:
            db.session.add(department)
            db.session.commit()
            db.session.refresh(department)
            return department
        except Exception as e:
            db.session.rollback()
            raise e

    def update_department(self, department):
        try:
            db.session.commit()
            db.session.refresh(department)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_department(self, department):
        try:
            db.session.delete(department)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

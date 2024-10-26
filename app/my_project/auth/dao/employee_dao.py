from my_project.auth.domain.employee import Employee
from db import db

class EmployeeDAO:
    def __init__(self):
        pass

    def get_all_employees(self):
        return Employee.query.all()

    def get_employee_by_id(self, employee_id: int):
        return Employee.query.get(employee_id)

    def create_employee(self, employee: Employee):
        try:
            db.session.add(employee)
            db.session.commit()
            db.session.refresh(employee)
            return employee
        except Exception as e:
            db.session.rollback()
            raise e

    def update_employee(self, employee):
        try:
            db.session.commit()
            db.session.refresh(employee)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_employee(self, employee):
        try:
            db.session.delete(employee)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

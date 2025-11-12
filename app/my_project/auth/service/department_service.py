from app.my_project.auth.dao.department_dao import DepartmentDAO
from app.my_project.auth.domain.department import Department

class DepartmentService:
    def __init__(self):
        self.department_dao = DepartmentDAO()

    def get_all_departments(self):
        return self.department_dao.get_all_departments()

    def get_department_by_id(self, department_id):
        return self.department_dao.get_department_by_id(department_id)

    def create_department(self, data):
        department_name = data.get('department_name')
        if not department_name:
            raise ValueError("Missing required field: department_name")
        
        department = Department(department_name=department_name)
        return self.department_dao.add_department(department)

    def update_department(self, department_id, data):
        department = self.get_department_by_id(department_id)
        if department:
            department.department_name = data.get('department_name', department.department_name)
            return self.department_dao.update_department(department)
        else:
            raise ValueError("Department not found")

    def delete_department(self, department_id):
        department = self.get_department_by_id(department_id)
        if department:
            return self.department_dao.delete_department(department)
        else:
            raise ValueError("Department not found")

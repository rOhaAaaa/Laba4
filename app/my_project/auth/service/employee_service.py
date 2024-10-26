from my_project.auth.dao.employee_dao import EmployeeDAO

class EmployeeService:
    def __init__(self):
        self.employee_dao = EmployeeDAO()

    def get_all_employees(self):
        return self.employee_dao.get_all_employees()

    def get_employee_by_id(self, employee_id):
        return self.employee_dao.get_employee_by_id(employee_id)

    def create_employee(self, data):
        return self.employee_dao.create_employee(data)

    def update_employee(self, employee_id, data):
        return self.employee_dao.update_employee(employee_id, data)

    def delete_employee(self, employee_id):
        return self.employee_dao.delete_employee(employee_id)

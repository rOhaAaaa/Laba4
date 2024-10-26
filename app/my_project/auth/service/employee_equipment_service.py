from my_project.auth.dao.employee_equipment_dao import EmployeeEquipmentDAO

class EmployeeEquipmentService:
    def __init__(self):
        self.employee_equipment_dao = EmployeeEquipmentDAO()

    def get_all_employee_equipments(self):
        return self.employee_equipment_dao.get_all_employee_equipments()

    def get_employee_equipment_by_id(self, employee_id):
        return self.employee_equipment_dao.get_employee_equipment_by_id(employee_id)

    def create_employee_equipment(self, data):
        return self.employee_equipment_dao.create_employee_equipment(data)

    def update_employee_equipment(self, employee_id, data):
        return self.employee_equipment_dao.update_employee_equipment(employee_id, data)

    def delete_employee_equipment(self, employee_id):
        return self.employee_equipment_dao.delete_employee_equipment(employee_id)

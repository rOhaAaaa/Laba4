from my_project.auth.domain.employee_equipment import EmployeeEquipment
from db import db

class EmployeeEquipmentDAO:
    def __init__(self):
        pass

    def get_all_employee_equipments(self):
        return EmployeeEquipment.query.all()

    def get_employee_equipment_by_employee_id(self, employee_id: int):
        return EmployeeEquipment.query.filter(EmployeeEquipment.employee_id == employee_id).first()

    def add_employee_equipment(self, employee_equipment: EmployeeEquipment):
        try:
            db.session.add(employee_equipment)
            db.session.commit()
            db.session.refresh(employee_equipment)
            return employee_equipment
        except Exception as e:
            db.session.rollback()
            raise e

    def update_employee_equipment(self, employee_equipment):
        try:
            db.session.commit()
            db.session.refresh(employee_equipment)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_employee_equipment(self, employee_equipment):
        try:
            db.session.delete(employee_equipment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

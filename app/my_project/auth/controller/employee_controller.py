import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.employee_dao import EmployeeDAO
from my_project.auth.domain.employee import Employee
from my_project.auth.dao.department_dao import DepartmentDAO
from my_project.auth.dao.printer_dao import PrinterDAO
from db import db

employee_bp = Blueprint('employee', __name__)
employee_dao = EmployeeDAO()
department_dao = DepartmentDAO()

@employee_bp.route('/', methods=['GET'])
def get_all_employees():
    employees = employee_dao.get_all_employees()
    return jsonify([employee.to_dict() for employee in employees]), 200

@employee_bp.route('/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = employee_dao.get_employee_by_id(id)
    if employee:
        return jsonify(employee.to_dict()), 200
    return jsonify({"message": "Employee not found"}), 404

@employee_bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    try:
        department_id = data.get('department_id')
        if department_id:
            department = department_dao.get_department_by_id(department_id)
            if not department:
                return jsonify({"error": "Invalid department_id"}), 400

        new_employee = Employee(
            name=data['name'],
            surname=data['surname'],
            position=data['position'],
            office_id=data.get('office_id'),
            department_id=department_id 
        )
        employee_dao.create_employee(new_employee)
        return jsonify({"message": "Employee created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    employee = employee_dao.get_employee_by_id(id)
    if employee:
        try:
            department_id = data.get('department_id')
            if department_id:
                department = department_dao.get_department_by_id(department_id)
                if not department:
                    return jsonify({"error": "Invalid department_id"}), 400

            employee.name = data.get('name', employee.name)
            employee.surname = data.get('surname', employee.surname)
            employee.position = data.get('position', employee.position)
            employee.office_id = data.get('office_id', employee.office_id)
            employee.department_id = department_id if department_id is not None else employee.department_id

            employee_dao.update_employee(employee)
            return jsonify({"message": "Employee updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Employee not found"}), 404

@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = employee_dao.get_employee_by_id(id)
    if employee:
        try:
            employee_dao.delete_employee(employee)
            return jsonify({"message": "Employee deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Employee not found"}), 404

@employee_bp.route('/<int:id>/printers', methods=['GET'])
def get_printers_of_employee(id):
    employee = employee_dao.get_employee_by_id(id)
    if employee:
        try:
            printers = [printer.to_dict() for printer in employee.printers]
            return jsonify({"employee_id": employee.employee_id, "printers": printers}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Employee not found"}), 404

@employee_bp.route('/employee_project/add_procedure', methods=['POST'])
def add_employee_project_via_procedure():
    data = request.get_json()
    if not data or 'employee_surname' not in data or 'project_name' not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        sql_query = """
        CALL insert_employee_project_link(%s, %s)
        """
        db.session.execute(sql_query, (data['employee_surname'], data['project_name']))
        db.session.commit()
        return jsonify({"message": "Employee-Project link created via procedure"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.employee_dao import EmployeeDAO
from my_project.auth.domain.employee import Employee
from my_project.auth.dao.printer_dao import PrinterDAO

employee_bp = Blueprint('employee', __name__)
employee_dao = EmployeeDAO()

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
        new_employee = Employee(
            name=data['name'],
            surname=data['surname'],
            position=data['position'],
            office_id=data['office_id']
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
            employee.name = data.get('name', employee.name)
            employee.position = data.get('position', employee.position)
            employee.office_id = data.get('office_id', employee.office_id)
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


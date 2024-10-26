import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.employee_equipment_dao import EmployeeEquipmentDAO
from my_project.auth.domain.employee_equipment import EmployeeEquipment
from my_project.auth.domain.employee import Employee
from my_project.auth.domain.office import Office
from my_project.auth.domain.computer import Computer
from my_project.auth.domain.monitor import Monitor
from my_project.auth.domain.ip_phone import IPPhone
from my_project.auth.domain.printer import Printer
from my_project.auth.domain.router import Router
from my_project.auth.domain.access_point import AccessPoint

employee_equipment_bp = Blueprint('employee_equipment', __name__)
employee_equipment_dao = EmployeeEquipmentDAO()

@employee_equipment_bp.route('/employee_equipments', methods=['GET'])
def get_all_employee_equipments():
    employee_equipments = employee_equipment_dao.get_all_employee_equipments()
    return jsonify([equipment.to_dict() for equipment in employee_equipments]), 200

@employee_equipment_bp.route('/employee_equipment/<int:employee_id>', methods=['GET'])
def get_employee_equipment_by_id(employee_id):
    equipment = employee_equipment_dao.get_employee_equipment_by_employee_id(employee_id)
    if equipment:
        return jsonify(equipment.to_dict()), 200
    return jsonify({"message": "Employee equipment not found"}), 404

@employee_equipment_bp.route('/employee_equipment', methods=['POST'])
def create_employee_equipment():
    data = request.get_json()
    try:
        if not Employee.query.get(data['employee_id']):
            return jsonify({"error": f"Employee with id {data['employee_id']} does not exist."}), 404
        if not Computer.query.get(data['computer_id']):
            return jsonify({"error": f"Computer with id {data['computer_id']} does not exist."}), 404
        if not Monitor.query.get(data['monitor_id']):
            return jsonify({"error": f"Monitor with id {data['monitor_id']} does not exist."}), 404
        if not IPPhone.query.get(data['phone_id']):
            return jsonify({"error": f"IP Phone with id {data['phone_id']} does not exist."}), 404
        if not Office.query.get(data['office_id']):
            return jsonify({"error": f"Office with id {data['office_id']} does not exist."}), 404
        if not Printer.query.get(data['printer_id']):
            return jsonify({"error": f"Printer with id {data['printer_id']} does not exist."}), 404
        if not Router.query.get(data['router_id']):
            return jsonify({"error": f"Router with id {data['router_id']} does not exist."}), 404
        if not AccessPoint.query.get(data['access_point_id']):
            return jsonify({"error": f"Access Point with id {data['access_point_id']} does not exist."}), 404

        new_equipment = EmployeeEquipment(
            employee_id=data['employee_id'],
            computer_id=data['computer_id'],
            monitor_id=data['monitor_id'],
            phone_id=data['phone_id'],
            office_id=data['office_id'],
            printer_id=data['printer_id'],
            router_id=data['router_id'],
            access_point_id=data['access_point_id'],
            issue_date=data['issue_date']
        )
        employee_equipment_dao.add_employee_equipment(new_equipment)  
        return jsonify({"message": "Employee equipment created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_equipment_bp.route('/employee_equipment/<int:employee_id>', methods=['PUT'])
def update_employee_equipment(employee_id):
    data = request.get_json()
    equipment = employee_equipment_dao.get_employee_equipment_by_employee_id(employee_id)
    if equipment:
        try:
            equipment.computer_id = data.get('computer_id', equipment.computer_id)
            equipment.monitor_id = data.get('monitor_id', equipment.monitor_id)
            equipment.phone_id = data.get('phone_id', equipment.phone_id)
            equipment.office_id = data.get('office_id', equipment.office_id)
            equipment.printer_id = data.get('printer_id', equipment.printer_id)
            equipment.router_id = data.get('router_id', equipment.router_id)
            equipment.access_point_id = data.get('access_point_id', equipment.access_point_id)
            equipment.issue_date = data.get('issue_date', equipment.issue_date)
            employee_equipment_dao.update_employee_equipment(equipment)
            return jsonify({"message": "Employee equipment updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Employee equipment not found"}), 404

@employee_equipment_bp.route('/employee_equipment/<int:employee_id>', methods=['DELETE'])
def delete_employee_equipment(employee_id):
    equipment = employee_equipment_dao.get_employee_equipment_by_employee_id(employee_id)
    if equipment:
        try:
            employee_equipment_dao.delete_employee_equipment(equipment)
            return jsonify({"message": "Employee equipment deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Employee equipment not found"}), 404

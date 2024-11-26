import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.department_dao import DepartmentDAO
from my_project.auth.domain.department import Department

department_bp = Blueprint('department', __name__)
department_dao = DepartmentDAO()

@department_bp.route('/departments', methods=['GET'])
def get_all_departments():
    departments = department_dao.get_all_departments()
    return jsonify([department.to_dict() for department in departments]), 200

@department_bp.route('/department/<int:id>', methods=['GET'])
def get_department_by_id(id):
    department = department_dao.get_department_by_id(id)
    if department:
        return jsonify(department.to_dict()), 200
    return jsonify({"message": "Department not found"}), 404

@department_bp.route('/department', methods=['POST'])
def create_department():
    data = request.get_json()
    try:
        if 'department_name' not in data:
            return jsonify({"error": "Missing required field: department_name"}), 400

        new_department = Department(
            department_name=data['department_name']
        )
        department_dao.add_department(new_department)
        return jsonify({"message": "Department created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@department_bp.route('/department/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()
    department = department_dao.get_department_by_id(id)
    if department:
        try:
            if 'department_name' not in data:
                return jsonify({"error": "No data provided to update"}), 400

            department.department_name = data.get('department_name', department.department_name)
            department_dao.update_department(department)
            return jsonify({"message": "Department updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Department not found"}), 404

@department_bp.route('/department/<int:id>', methods=['DELETE'])
def delete_department(id):
    department = department_dao.get_department_by_id(id)
    if department:
        try:
            department_dao.delete_department(department)
            return jsonify({"message": "Department deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete department: {str(e)}"}), 500
    return jsonify({"message": "Department not found"}), 404
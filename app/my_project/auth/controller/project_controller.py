import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.employee_dao import EmployeeDAO
from my_project.auth.dao.project_dao import ProjectDAO
from my_project.auth.domain.project import Project
from my_project.auth.service.project_service import ProjectService

from db import db

project_bp = Blueprint('project', __name__)
employee_dao = EmployeeDAO()
project_service = ProjectService()

@project_bp.route('/projects', methods=['GET'])
def get_all_projects():
    projects = project_service.get_all_projects()
    return jsonify([project.to_dict() for project in projects]), 200

@project_bp.route('/project/<int:id>', methods=['GET'])
def get_project_by_id(id):
    project = project_service.get_project_by_id(id)
    if project:
        return jsonify(project.to_dict()), 200
    return jsonify({"message": "Project not found"}), 404

@project_bp.route('/project', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or 'project_name' not in data:
        return jsonify({"error": "Missing required fields: 'project_name'"}), 400
    try:
        new_project = Project(
            project_name=data['project_name'],
            description=data.get('description')
        )
        project_service.create_project(new_project)
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@project_bp.route('/project/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    project = project_service.get_project_by_id(id)
    if project:
        try:
            project.project_name = data.get('project_name', project.project_name)
            project.description = data.get('description', project.description)
            project_service.update_project(project)
            return jsonify({"message": "Project updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Project not found"}), 404

@project_bp.route('/project/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = project_service.get_project_by_id(id)
    if project:
        try:
            project_service.delete_project(project)
            return jsonify({"message": "Project deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Project not found"}), 404

@project_bp.route('/add_employee_to_project', methods=['POST'])
def add_employee_to_project():
    data = request.get_json()
    emp_name = data.get('name')
    emp_surname = data.get('surname')
    proj_name = data.get('project_name')

    try:
        query = "CALL AddEmployeeToProject(%s, %s, %s)"
        db.session.execute(query, (emp_name, emp_surname, proj_name))
        db.session.commit()
        return jsonify({"message": "Employee added to project successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@project_bp.route('/project/<int:id>/employees', methods=['GET'])
def get_employees_of_project(id):
    project = project_service.get_project_by_id(id)
    if project:
        try:
            employees = [employee.to_dict() for employee in project.employees]
            return jsonify({"project_id": project.project_id, "employees": employees}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Project not found"}), 404
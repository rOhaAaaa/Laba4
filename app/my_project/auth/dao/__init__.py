from flask import Blueprint, request, jsonify
from app.db import db

employee_project_bp = Blueprint('employee_project', __name__)

@employee_project_bp.route('/employee_project/add_procedure', methods=['POST'])
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

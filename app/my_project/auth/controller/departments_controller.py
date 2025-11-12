from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.department_dao import DepartmentDAO
from app.my_project.auth.domain.department import Department

department_bp = Blueprint("department", __name__)
department_dao = DepartmentDAO()


@department_bp.get("/")
@swag_from({
    "tags": ["Departments"],
    "summary": "Get all departments",
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "minimum": 1},
            "description": "Page number (optional, naive slicing on server)"
        },
        {
            "name": "page_size",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "minimum": 1, "maximum": 500},
            "description": "Items per page (optional)"
        }
    ],
    "responses": {
        "200": {
            "description": "List of departments",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"department_id": 1, "department_name": "IT"}
                        ],
                        "total": 1,
                        "page": 1,
                        "page_size": 50
                    }
                }
            }
        }
    }
})
def get_all_departments():
    """Return all departments (with optional naive pagination)."""
    departments = department_dao.get_all_departments()
    items = [d.to_dict() for d in departments]

    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", len(items) or 1))
        page = max(page, 1)
        page_size = max(min(page_size, 500), 1)
    except ValueError:
        page, page_size = 1, len(items) or 1

    start = (page - 1) * page_size
    end = start + page_size
    return jsonify({
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "page_size": page_size
    }), 200


@department_bp.get("/<int:id>")
@swag_from({
    "tags": ["Departments"],
    "summary": "Get department by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Department found",
            "content": {
                "application/json": {
                    "example": {"department_id": 1, "department_name": "IT"}
                }
            }
        },
        "404": {"description": "Department not found"}
    }
})
def get_department_by_id(id: int):
    department = department_dao.get_department_by_id(id)
    if department:
        return jsonify(department.to_dict()), 200
    return jsonify({"message": "Department not found"}), 404


@department_bp.post("/")
@swag_from({
    "tags": ["Departments"],
    "summary": "Create department",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["department_name"],
                    "properties": {
                        "department_name": {"type": "string"}
                    }
                },
                "example": {
                    "department_name": "Finance"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Department created"},
        "400": {"description": "Validation error"}
    }
})
def create_department():
    data = request.get_json(silent=True) or {}
    if not data.get("department_name"):
        return jsonify({"error": "'department_name' is required"}), 400

    try:
        new_department = Department(department_name=data["department_name"])
        department_dao.add_department(new_department)
        return jsonify({"message": "Department created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@department_bp.put("/<int:id>")
@swag_from({
    "tags": ["Departments"],
    "summary": "Update department",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "department_name": {"type": "string"}
                    }
                },
                "example": {
                    "department_name": "Human Resources"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Department updated"},
        "404": {"description": "Department not found"},
        "400": {"description": "Validation error"}
    }
})
def update_department(id: int):
    data = request.get_json(silent=True) or {}
    department = department_dao.get_department_by_id(id)
    if not department:
        return jsonify({"message": "Department not found"}), 404

    try:
        if "department_name" not in data:
            return jsonify({"error": "No data provided to update"}), 400

        department.department_name = data.get("department_name", department.department_name)
        department_dao.update_department(department)
        return jsonify({"message": "Department updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@department_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Departments"],
    "summary": "Delete department",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Department deleted"},
        "404": {"description": "Department not found"}
    }
})
def delete_department(id: int):
    department = department_dao.get_department_by_id(id)
    if not department:
        return jsonify({"message": "Department not found"}), 404

    try:
        department_dao.delete_department(department)
        return jsonify({"message": "Department deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete department: {str(e)}"}), 500

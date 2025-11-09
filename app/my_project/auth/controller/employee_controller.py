from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy import text

from app.db import db
from app.my_project.auth.dao.employee_dao import EmployeeDAO
from app.my_project.auth.dao.department_dao import DepartmentDAO
from app.my_project.auth.domain.employee import Employee

employee_bp = Blueprint("employee", __name__)
employee_dao = EmployeeDAO()
department_dao = DepartmentDAO()


@employee_bp.get("/")
@swag_from({
    "tags": ["Employees"],
    "summary": "Get all employees",
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
            "description": "List of employees",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"employee_id": 1, "name": "John", "surname": "Doe", "position": "Dev"}
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
def get_all_employees():
    """Return all employees (with optional naive pagination)."""
    employees = employee_dao.get_all_employees()  # очікується список моделей
    items = [e.to_dict() for e in employees]

    # наївна пагінація, якщо користувач просить
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


@employee_bp.get("/<int:id>")
@swag_from({
    "tags": ["Employees"],
    "summary": "Get employee by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Employee found",
            "content": {"application/json": {"example": {"employee_id": 1, "name": "John", "surname": "Doe"}}}
        },
        "404": {"description": "Employee not found"}
    }
})
def get_employee_by_id(id: int):
    employee = employee_dao.get_employee_by_id(id)
    if employee:
        return jsonify(employee.to_dict()), 200
    return jsonify({"message": "Employee not found"}), 404


@employee_bp.post("/")
@swag_from({
    "tags": ["Employees"],
    "summary": "Create employee",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["name", "surname", "position"],
                    "properties": {
                        "name": {"type": "string"},
                        "surname": {"type": "string"},
                        "position": {"type": "string"},
                        "office_id": {"type": "integer"},
                        "department_id": {"type": "integer"}
                    }
                },
                "example": {
                    "name": "John",
                    "surname": "Doe",
                    "position": "Developer",
                    "office_id": 1,
                    "department_id": 2
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Employee created"},
        "400": {"description": "Validation error"}
    }
})
def create_employee():
    data = request.get_json(silent=True) or {}
    # валідація
    for field in ("name", "surname", "position"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        department_id = data.get("department_id")
        if department_id is not None:
            department = department_dao.get_department_by_id(department_id)
            if not department:
                return jsonify({"error": "Invalid department_id"}), 400

        new_employee = Employee(
            name=data["name"],
            surname=data["surname"],
            position=data["position"],
            office_id=data.get("office_id"),
            department_id=department_id
        )
        employee_dao.create_employee(new_employee)
        return jsonify({"message": "Employee created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@employee_bp.put("/<int:id>")
@swag_from({
    "tags": ["Employees"],
    "summary": "Update employee",
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
                        "name": {"type": "string"},
                        "surname": {"type": "string"},
                        "position": {"type": "string"},
                        "office_id": {"type": "integer"},
                        "department_id": {"type": "integer"}
                    }
                },
                "example": {
                    "name": "Jane",
                    "surname": "Doe",
                    "position": "Lead Dev",
                    "office_id": 2,
                    "department_id": 3
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Employee updated"},
        "404": {"description": "Employee not found"},
        "400": {"description": "Validation error"}
    }
})
def update_employee(id: int):
    data = request.get_json(silent=True) or {}
    employee = employee_dao.get_employee_by_id(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    try:
        department_id = data.get("department_id")
        if department_id is not None:
            department = department_dao.get_department_by_id(department_id)
            if not department:
                return jsonify({"error": "Invalid department_id"}), 400

        employee.name = data.get("name", employee.name)
        employee.surname = data.get("surname", employee.surname)
        employee.position = data.get("position", employee.position)
        employee.office_id = data.get("office_id", employee.office_id)
        if department_id is not None:
            employee.department_id = department_id

        employee_dao.update_employee(employee)
        return jsonify({"message": "Employee updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@employee_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Employees"],
    "summary": "Delete employee",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Employee deleted"},
        "404": {"description": "Employee not found"}
    }
})
def delete_employee(id: int):
    employee = employee_dao.get_employee_by_id(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    try:
        employee_dao.delete_employee(employee)
        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@employee_bp.get("/<int:id>/printers")
@swag_from({
    "tags": ["Employees"],
    "summary": "Get printers assigned to an employee",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Printers list for employee",
            "content": {
                "application/json": {
                    "example": {
                        "employee_id": 1,
                        "printers": [{"printer_id": 10, "model": "HP 402"}]
                    }
                }
            }
        },
        "404": {"description": "Employee not found"}
    }
})
def get_printers_of_employee(id: int):
    employee = employee_dao.get_employee_by_id(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    try:
        printers = [printer.to_dict() for printer in getattr(employee, "printers", [])]
        return jsonify({"employee_id": getattr(employee, "employee_id", id), "printers": printers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.post("/employee_project/add_procedure")
@swag_from({
    "tags": ["Employees"],
    "summary": "Link employee to project via stored procedure",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["employee_surname", "project_name"],
                    "properties": {
                        "employee_surname": {"type": "string"},
                        "project_name": {"type": "string"}
                    }
                },
                "example": {
                    "employee_surname": "Doe",
                    "project_name": "Intranet Revamp"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Employee-Project link created via procedure"},
        "400": {"description": "Validation error"}
    }
})
def add_employee_project_via_procedure():
    data = request.get_json(silent=True) or {}
    if not data.get("employee_surname") or not data.get("project_name"):
        return jsonify({"error": "Invalid data"}), 400

    try:
        stmt = text("CALL insert_employee_project_link(:employee_surname, :project_name)")
        db.session.execute(stmt, {
            "employee_surname": data["employee_surname"],
            "project_name": data["project_name"]
        })
        db.session.commit()
        return jsonify({"message": "Employee-Project link created via procedure"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy import text

from app.db import db
from app.my_project.auth.domain.project import Project
from app.my_project.auth.service.project_service import ProjectService

project_bp = Blueprint("project", __name__)
project_service = ProjectService()


@project_bp.get("/")
@swag_from({
    "tags": ["Projects"],
    "summary": "Get all projects",
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
            "description": "List of projects",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"project_id": 1, "project_name": "Intranet Revamp", "description": "Phase 1"}
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
def get_all_projects():
    """Return all projects (with optional naive pagination)."""
    projects = project_service.get_all_projects()
    items = [p.to_dict() for p in projects]

    # наївна пагінація
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


@project_bp.get("/<int:id>")
@swag_from({
    "tags": ["Projects"],
    "summary": "Get project by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Project found",
            "content": {
                "application/json": {
                    "example": {"project_id": 1, "project_name": "Intranet Revamp", "description": "Phase 1"}
                }
            }
        },
        "404": {"description": "Project not found"}
    }
})
def get_project_by_id(id: int):
    project = project_service.get_project_by_id(id)
    if project:
        return jsonify(project.to_dict()), 200
    return jsonify({"message": "Project not found"}), 404


@project_bp.post("/")
@swag_from({
    "tags": ["Projects"],
    "summary": "Create project",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["project_name"],
                    "properties": {
                        "project_name": {"type": "string"},
                        "description": {"type": "string"}
                    }
                },
                "example": {
                    "project_name": "CRM Migration",
                    "description": "Move to cloud CRM"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Project created"},
        "400": {"description": "Validation error"}
    }
})
def create_project():
    data = request.get_json(silent=True) or {}
    if not data.get("project_name"):
        return jsonify({"error": "'project_name' is required"}), 400

    try:
        new_project = Project(
            project_name=data["project_name"],
            description=data.get("description")
        )
        project_service.create_project(new_project)
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_bp.put("/<int:id>")
@swag_from({
    "tags": ["Projects"],
    "summary": "Update project",
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
                        "project_name": {"type": "string"},
                        "description": {"type": "string"}
                    }
                },
                "example": {
                    "project_name": "CRM Migration - Phase 2",
                    "description": "Reporting and training"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Project updated"},
        "404": {"description": "Project not found"},
        "400": {"description": "Validation error"}
    }
})
def update_project(id: int):
    data = request.get_json(silent=True) or {}
    project = project_service.get_project_by_id(id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    try:
        project.project_name = data.get("project_name", project.project_name)
        project.description = data.get("description", project.description)
        project_service.update_project(project)
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Projects"],
    "summary": "Delete project",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Project deleted"},
        "404": {"description": "Project not found"}
    }
})
def delete_project(id: int):
    project = project_service.get_project_by_id(id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    try:
        project_service.delete_project(project)
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_bp.post("/add_employee_to_project")
@swag_from({
    "tags": ["Projects"],
    "summary": "Add employee to project via stored procedure",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["name", "surname", "project_name"],
                    "properties": {
                        "name": {"type": "string"},
                        "surname": {"type": "string"},
                        "project_name": {"type": "string"}
                    }
                },
                "example": {
                    "name": "John",
                    "surname": "Doe",
                    "project_name": "CRM Migration"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Employee added to project"},
        "400": {"description": "Validation error"}
    }
})
def add_employee_to_project():
    data = request.get_json(silent=True) or {}
    if not all(data.get(k) for k in ("name", "surname", "project_name")):
        return jsonify({"error": "Missing required fields: 'name', 'surname', 'project_name'"}), 400

    try:
        # Виклик процедури через SQLAlchemy text з іменованими параметрами
        stmt = text("CALL AddEmployeeToProject(:name, :surname, :project_name)")
        db.session.execute(stmt, {
            "name": data["name"],
            "surname": data["surname"],
            "project_name": data["project_name"]
        })
        db.session.commit()
        return jsonify({"message": "Employee added to project successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_bp.get("/<int:id>/employees")
@swag_from({
    "tags": ["Projects"],
    "summary": "Get employees assigned to a project",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Employees list for the project",
            "content": {
                "application/json": {
                    "example": {
                        "project_id": 1,
                        "employees": [
                            {"employee_id": 1, "name": "John", "surname": "Doe", "position": "Dev"}
                        ]
                    }
                }
            }
        },
        "404": {"description": "Project not found"}
    }
})
def get_employees_of_project(id: int):
    project = project_service.get_project_by_id(id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    try:
        employees = [e.to_dict() for e in getattr(project, "employees", [])]
        return jsonify({"project_id": getattr(project, "project_id", id), "employees": employees}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

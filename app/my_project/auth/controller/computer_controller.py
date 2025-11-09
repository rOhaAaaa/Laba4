from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy import text

from app.db import db
from app.my_project.auth.dao.computer_dao import ComputerDAO
from app.my_project.auth.domain.computer import Computer

computer_bp = Blueprint("computer", __name__)
computer_dao = ComputerDAO()


@computer_bp.get("/")
@swag_from({
    "tags": ["Computers"],
    "summary": "Get all computers",
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
            "description": "List of computers",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "computer_id": 1,
                                "model_name": "Dell OptiPlex",
                                "operating_system": "Windows 11",
                                "config_id": 3
                            }
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
def get_all_computers():
    """Return all computers (with optional naive pagination)."""
    computers = computer_dao.get_all_computers()
    items = [c.to_dict() for c in computers]

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


@computer_bp.get("/<int:id>")
@swag_from({
    "tags": ["Computers"],
    "summary": "Get computer by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Computer found",
            "content": {
                "application/json": {
                    "example": {
                        "computer_id": 1,
                        "model_name": "Dell OptiPlex",
                        "operating_system": "Windows 11",
                        "config_id": 3
                    }
                }
            }
        },
        "404": {"description": "Computer not found"}
    }
})
def get_computer_by_id(id: int):
    computer = computer_dao.get_computer_by_id(id)
    if computer:
        return jsonify(computer.to_dict()), 200
    return jsonify({"message": "Computer not found"}), 404


@computer_bp.post("/")
@swag_from({
    "tags": ["Computers"],
    "summary": "Create computer",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["model_name", "operating_system"],
                    "properties": {
                        "model_name": {"type": "string"},
                        "operating_system": {"type": "string"},
                        "config_id": {"type": "integer"}
                    }
                },
                "example": {
                    "model_name": "HP ProDesk 600",
                    "operating_system": "Ubuntu 22.04",
                    "config_id": 5
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Computer created"},
        "400": {"description": "Validation error"}
    }
})
def create_computer():
    data = request.get_json(silent=True) or {}
    # валідація
    for field in ("model_name", "operating_system"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_computer = Computer(
            model_name=data["model_name"],
            operating_system=data["operating_system"],
            config_id=data.get("config_id")
        )
        computer_dao.add_computer(new_computer)
        return jsonify({"message": "Computer created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@computer_bp.put("/<int:id>")
@swag_from({
    "tags": ["Computers"],
    "summary": "Update computer",
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
                        "model_name": {"type": "string"},
                        "operating_system": {"type": "string"},
                        "config_id": {"type": "integer"}
                    }
                },
                "example": {
                    "model_name": "Lenovo ThinkCentre",
                    "operating_system": "Windows 10",
                    "config_id": 2
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Computer updated"},
        "404": {"description": "Computer not found"},
        "400": {"description": "Validation error"}
    }
})
def update_computer(id: int):
    data = request.get_json(silent=True) or {}
    computer = computer_dao.get_computer_by_id(id)
    if not computer:
        return jsonify({"message": "Computer not found"}), 404

    try:
        computer.model_name = data.get("model_name", computer.model_name)
        computer.operating_system = data.get("operating_system", computer.operating_system)
        computer.config_id = data.get("config_id", computer.config_id)

        computer_dao.update_computer(computer)
        return jsonify({"message": "Computer updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@computer_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Computers"],
    "summary": "Delete computer",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Computer deleted"},
        "404": {"description": "Computer not found"}
    }
})
def delete_computer(id: int):
    computer = computer_dao.get_computer_by_id(id)
    if not computer:
        return jsonify({"message": "Computer not found"}), 404

    try:
        computer_dao.delete_computer(computer)
        return jsonify({"message": "Computer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete computer: {str(e)}"}), 500


@computer_bp.get("/with_configurations")
@swag_from({
    "tags": ["Computers"],
    "summary": "Get computers with configurations",
    "responses": {
        "200": {
            "description": "List of computers with optional configuration objects",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "computer_id": 1,
                            "model_name": "Dell OptiPlex",
                            "operating_system": "Windows 11",
                            "configuration": {
                                "config_id": 3,
                                "cpu": "i7-12700",
                                "ram_gb": 32
                            }
                        }
                    ]
                }
            }
        }
    }
})
def get_computers_with_configurations():
    computers = computer_dao.get_all_computers()
    result = [
        {
            "computer_id": c.computer_id,
            "model_name": c.model_name,
            "operating_system": c.operating_system,
            "configuration": c.configuration.to_dict() if getattr(c, "configuration", None) else None
        }
        for c in computers
    ]
    return jsonify(result), 200


@computer_bp.post("/create_dynamic_tables")
@swag_from({
    "tags": ["Computers"],
    "summary": "Create dynamic computer tables and distribute data (stored procedure)",
    "responses": {
        "201": {"description": "Dynamic tables created and data distributed"},
        "500": {"description": "Internal server error"}
    }
})
def create_dynamic_computer_tables():
    try:
        stmt = text("CALL create_dynamic_computer_tables_and_distribute_data()")
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": "Dynamic tables created and data distributed successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

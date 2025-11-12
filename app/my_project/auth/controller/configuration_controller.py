from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.configuration_dao import ConfigurationDAO
from app.my_project.auth.domain.configuration import Configuration

configuration_bp = Blueprint("configuration", __name__)
configuration_dao = ConfigurationDAO()


@configuration_bp.get("/")
@swag_from({
    "tags": ["Configurations"],
    "summary": "Get all configurations",
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
            "description": "List of configurations",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"config_id": 1, "processor": "i5-12400", "ram": "16GB", "hard_drive": "512GB SSD"}
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
def get_all_configurations():
    """Return all configurations (with optional naive pagination)."""
    configurations = configuration_dao.get_all_configurations()
    items = [c.to_dict() for c in configurations]

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


@configuration_bp.get("/<int:id>")
@swag_from({
    "tags": ["Configurations"],
    "summary": "Get configuration by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Configuration found",
            "content": {
                "application/json": {
                    "example": {"config_id": 1, "processor": "i5-12400", "ram": "16GB", "hard_drive": "512GB SSD"}
                }
            }
        },
        "404": {"description": "Configuration not found"}
    }
})
def get_configuration_by_id(id: int):
    configuration = configuration_dao.get_configuration_by_id(id)
    if configuration:
        return jsonify(configuration.to_dict()), 200
    return jsonify({"message": "Configuration not found"}), 404


@configuration_bp.post("/")
@swag_from({
    "tags": ["Configurations"],
    "summary": "Create configuration",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["processor", "ram", "hard_drive"],
                    "properties": {
                        "processor": {"type": "string"},
                        "ram": {"type": "string"},
                        "hard_drive": {"type": "string"}
                    }
                },
                "example": {
                    "processor": "Ryzen 5 5600",
                    "ram": "32GB",
                    "hard_drive": "1TB SSD"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Configuration created"},
        "400": {"description": "Validation error"}
    }
})
def create_configuration():
    data = request.get_json(silent=True) or {}
    for field in ("processor", "ram", "hard_drive"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_configuration = Configuration(
            processor=data["processor"],
            ram=data["ram"],
            hard_drive=data["hard_drive"]
        )
        configuration_dao.add_configuration(new_configuration)
        return jsonify({"message": "Configuration created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@configuration_bp.put("/<int:id>")
@swag_from({
    "tags": ["Configurations"],
    "summary": "Update configuration",
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
                        "processor": {"type": "string"},
                        "ram": {"type": "string"},
                        "hard_drive": {"type": "string"}
                    }
                },
                "example": {
                    "processor": "i7-13700",
                    "ram": "64GB",
                    "hard_drive": "2TB SSD"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Configuration updated"},
        "404": {"description": "Configuration not found"},
        "400": {"description": "Validation error"}
    }
})
def update_configuration(id: int):
    data = request.get_json(silent=True) or {}
    configuration = configuration_dao.get_configuration_by_id(id)
    if not configuration:
        return jsonify({"message": "Configuration not found"}), 404

    try:
        # якщо користувач нічого не передав — повертаємо помилку валідації
        if not any(k in data for k in ("processor", "ram", "hard_drive")):
            return jsonify({"error": "No data provided to update"}), 400

        configuration.processor = data.get("processor", configuration.processor)
        configuration.ram = data.get("ram", configuration.ram)
        configuration.hard_drive = data.get("hard_drive", configuration.hard_drive)

        configuration_dao.update_configuration(configuration)
        return jsonify({"message": "Configuration updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@configuration_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Configurations"],
    "summary": "Delete configuration",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Configuration deleted"},
        "404": {"description": "Configuration not found"}
    }
})
def delete_configuration(id: int):
    configuration = configuration_dao.get_configuration_by_id(id)
    if not configuration:
        return jsonify({"message": "Configuration not found"}), 404

    try:
        configuration_dao.delete_configuration(configuration)
        return jsonify({"message": "Configuration deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete configuration: {str(e)}"}), 500

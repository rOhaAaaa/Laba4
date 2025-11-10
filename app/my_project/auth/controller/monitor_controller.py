from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy import text

from app.db import db
from app.my_project.auth.dao.monitor_dao import MonitorDAO
from app.my_project.auth.domain.monitor import Monitor
from app.my_project.auth.service.generic_service import GenericService

monitor_bp = Blueprint("monitor", __name__)
monitor_dao = MonitorDAO()
service = GenericService()


@monitor_bp.get("/")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Get all monitors",
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
            "description": "List of monitors",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"monitor_id": 1, "model_name": "Dell U2720Q", "screen_size": 27}
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
def get_all_monitors():
    """Return all monitors (with optional naive pagination)."""
    monitors = monitor_dao.get_all_monitors()
    items = [m.to_dict() for m in monitors]

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


@monitor_bp.get("/<int:id>")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Get monitor by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Monitor found",
            "content": {
                "application/json": {
                    "example": {"monitor_id": 1, "model_name": "Dell U2720Q", "screen_size": 27}
                }
            }
        },
        "404": {"description": "Monitor not found"}
    }
})
def get_monitor_by_id(id: int):
    monitor = monitor_dao.get_monitor_by_id(id)
    if monitor:
        return jsonify(monitor.to_dict()), 200
    return jsonify({"message": "Monitor not found"}), 404


@monitor_bp.post("/")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Create monitor",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["model_name", "screen_size"],
                    "properties": {
                        "model_name": {"type": "string"},
                        "screen_size": {"type": "number"}
                    }
                },
                "example": {
                    "model_name": "LG 27UL850",
                    "screen_size": 27
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Monitor created"},
        "400": {"description": "Validation error"}
    }
})
def create_monitor():
    data = request.get_json(silent=True) or {}
    for field in ("model_name", "screen_size"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_monitor = Monitor(
            model_name=data["model_name"],
            screen_size=data["screen_size"]
        )
        monitor_dao.add_monitor(new_monitor)
        return jsonify({"message": "Monitor created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@monitor_bp.post("/add_procedure")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Insert monitor via stored procedure",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["model_name", "screen_size"],
                    "properties": {
                        "model_name": {"type": "string"},
                        "screen_size": {"type": "number"}
                    }
                },
                "example": {
                    "model_name": "Samsung S27A800",
                    "screen_size": 27
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Monitor inserted via procedure"},
        "400": {"description": "Validation error"}
    }
})
def add_monitor_via_procedure():
    data = request.get_json(silent=True) or {}
    if not data.get("model_name") or data.get("screen_size") is None:
        return jsonify({"error": "Invalid data"}), 400

    try:
        # Виклик процедури через SQLAlchemy text з іменованими параметрами
        stmt = text("CALL insert_into_monitor(:model_name, :screen_size)")
        db.session.execute(stmt, {
            "model_name": data["model_name"],
            "screen_size": data["screen_size"]
        })
        db.session.commit()
        return jsonify({"message": "Monitor added via procedure"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@monitor_bp.put("/<int:id>")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Update monitor",
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
                        "screen_size": {"type": "number"}
                    }
                },
                "example": {
                    "model_name": "Dell U2723QE",
                    "screen_size": 27
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Monitor updated"},
        "404": {"description": "Monitor not found"},
        "400": {"description": "Validation error"}
    }
})
def update_monitor(id: int):
    data = request.get_json(silent=True) or {}
    monitor = monitor_dao.get_monitor_by_id(id)
    if not monitor:
        return jsonify({"message": "Monitor not found"}), 404

    try:
        monitor.model_name = data.get("model_name", monitor.model_name)
        monitor.screen_size = data.get("screen_size", monitor.screen_size)
        monitor_dao.update_monitor(monitor)
        return jsonify({"message": "Monitor updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@monitor_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Delete monitor",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Monitor deleted"},
        "404": {"description": "Monitor not found"}
    }
})
def delete_monitor(id: int):
    monitor = monitor_dao.get_monitor_by_id(id)
    if not monitor:
        return jsonify({"message": "Monitor not found"}), 404

    try:
        monitor_dao.delete_monitor(monitor)
        return jsonify({"message": "Monitor deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@monitor_bp.post("/procedure/<procedure_name>")
@swag_from({
    "tags": ["Monitors"],
    "summary": "Execute arbitrary stored procedure by name",
    "parameters": [
        {
            "name": "procedure_name",
            "in": "path",
            "required": True,
            "schema": {"type": "string"}
        }
    ],
    "requestBody": {
        "required": False,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "params": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Positional parameters for the stored procedure"
                        }
                    }
                },
                "example": {
                    "params": ["param1", "param2"]
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Procedure executed",
            "content": {
                "application/json": {
                    "example": {"message": "Procedure executed", "results": [{"row": 1}]}
                }
            }
        }
    }
})
def call_procedure(procedure_name: str):
    try:
        payload = request.get_json(silent=True) or {}
        params = payload.get("params", [])
        results = service.execute_procedure(procedure_name, params)
        return jsonify({"message": "Procedure executed", "results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

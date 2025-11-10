from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.router_dao import RouterDAO
from app.my_project.auth.domain.router import Router

router_bp = Blueprint("router", __name__)
router_dao = RouterDAO()


@router_bp.get("/")
@swag_from({
    "tags": ["Routers"],
    "summary": "Get all routers",
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
            "description": "List of routers",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"router_id": 1, "model_name": "MikroTik hAP ac2", "connection_speed": 1000}
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
def get_all_routers():
    """Return all routers (with optional naive pagination)."""
    routers = router_dao.get_all_routers()
    items = [r.to_dict() for r in routers]

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


@router_bp.get("/<int:id>")
@swag_from({
    "tags": ["Routers"],
    "summary": "Get router by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Router found",
            "content": {
                "application/json": {
                    "example": {"router_id": 1, "model_name": "MikroTik hAP ac2", "connection_speed": 1000}
                }
            }
        },
        "404": {"description": "Router not found"}
    }
})
def get_router_by_id(id: int):
    router = router_dao.get_router_by_id(id)
    if router:
        return jsonify(router.to_dict()), 200
    return jsonify({"message": "Router not found"}), 404


@router_bp.post("/")
@swag_from({
    "tags": ["Routers"],
    "summary": "Create router",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["model_name", "connection_speed"],
                    "properties": {
                        "model_name": {"type": "string"},
                        "connection_speed": {"type": "number", "description": "Speed in Mbps"}
                    }
                },
                "example": {
                    "model_name": "TP-Link Archer AX55",
                    "connection_speed": 3000
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Router created"},
        "400": {"description": "Validation error"}
    }
})
def create_router():
    data = request.get_json(silent=True) or {}
    for field in ("model_name", "connection_speed"):
        if field not in data or data.get(field) in (None, ""):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_router = Router(
            model_name=data["model_name"],
            connection_speed=data["connection_speed"]
        )
        router_dao.add_router(new_router)
        return jsonify({"message": "Router created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@router_bp.put("/<int:id>")
@swag_from({
    "tags": ["Routers"],
    "summary": "Update router",
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
                        "connection_speed": {"type": "number"}
                    }
                },
                "example": {
                    "model_name": "ASUS RT-AX88U",
                    "connection_speed": 6000
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Router updated"},
        "404": {"description": "Router not found"},
        "400": {"description": "Validation error"}
    }
})
def update_router(id: int):
    data = request.get_json(silent=True) or {}
    router = router_dao.get_router_by_id(id)
    if not router:
        return jsonify({"message": "Router not found"}), 404

    try:
        router.model_name = data.get("model_name", router.model_name)
        router.connection_speed = data.get("connection_speed", router.connection_speed)
        router_dao.update_router(router)
        return jsonify({"message": "Router updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@router_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Routers"],
    "summary": "Delete router",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Router deleted"},
        "404": {"description": "Router not found"}
    }
})
def delete_router(id: int):
    router = router_dao.get_router_by_id(id)
    if not router:
        return jsonify({"message": "Router not found"}), 404

    try:
        router_dao.delete_router(router)
        return jsonify({"message": "Router deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.access_point_dao import AccessPointDAO
from app.my_project.auth.domain.access_point import AccessPoint

access_point_bp = Blueprint("access_point", __name__)
access_point_dao = AccessPointDAO()


@access_point_bp.get("/")
@swag_from({
    "tags": ["Access Points"],
    "summary": "Get all access points",
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
            "description": "List of access points",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"access_point_id": 1, "brand": "Ubiquiti", "model": "UAP-AC-LR", "serial_number": "SN123"}
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
def get_all_access_points():
    """Return all access points (with optional naive pagination)."""
    access_points = access_point_dao.get_all_access_points()
    items = [ap.to_dict() for ap in access_points]

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


@access_point_bp.get("/<int:id>")
@swag_from({
    "tags": ["Access Points"],
    "summary": "Get access point by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Access point found",
            "content": {
                "application/json": {
                    "example": {"access_point_id": 1, "brand": "Ubiquiti", "model": "UAP-AC-LR", "serial_number": "SN123"}
                }
            }
        },
        "404": {"description": "Access point not found"}
    }
})
def get_access_point_by_id(id: int):
    ap = access_point_dao.get_access_point_by_id(id)
    if ap:
        return jsonify(ap.to_dict()), 200
    return jsonify({"message": "Access Point not found"}), 404


@access_point_bp.post("/")
@swag_from({
    "tags": ["Access Points"],
    "summary": "Create access point",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["brand", "model", "serial_number"],
                    "properties": {
                        "brand": {"type": "string"},
                        "model": {"type": "string"},
                        "serial_number": {"type": "string"}
                    }
                },
                "example": {
                    "brand": "Ubiquiti",
                    "model": "UAP-AC-LR",
                    "serial_number": "SN123"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Access point created"},
        "400": {"description": "Validation error"}
    }
})
def create_access_point():
    data = request.get_json(silent=True) or {}
    for field in ("brand", "model", "serial_number"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_ap = AccessPoint(
            brand=data["brand"],
            model=data["model"],
            serial_number=data["serial_number"],
        )
        access_point_dao.create_access_point(new_ap)
        return jsonify({"message": "Access Point created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@access_point_bp.put("/<int:id>")
@swag_from({
    "tags": ["Access Points"],
    "summary": "Update access point",
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
                        "brand": {"type": "string"},
                        "model": {"type": "string"},
                        "serial_number": {"type": "string"}
                    }
                },
                "example": {
                    "brand": "TP-Link",
                    "model": "EAP245",
                    "serial_number": "SN999"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Access point updated"},
        "404": {"description": "Access point not found"},
        "400": {"description": "Validation error"}
    }
})
def update_access_point(id: int):
    data = request.get_json(silent=True) or {}
    ap = access_point_dao.get_access_point_by_id(id)
    if not ap:
        return jsonify({"message": "Access Point not found"}), 404

    try:
        ap.brand = data.get("brand", ap.brand)
        ap.model = data.get("model", ap.model)
        ap.serial_number = data.get("serial_number", ap.serial_number)

        access_point_dao.update_access_point(ap)
        return jsonify({"message": "Access Point updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@access_point_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Access Points"],
    "summary": "Delete access point",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Access point deleted"},
        "404": {"description": "Access point not found"}
    }
})
def delete_access_point(id: int):
    ap = access_point_dao.get_access_point_by_id(id)
    if not ap:
        return jsonify({"message": "Access Point not found"}), 404

    try:
        access_point_dao.delete_access_point(ap)
        return jsonify({"message": "Access Point deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

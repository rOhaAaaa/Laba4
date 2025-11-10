from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.office_dao import OfficeDAO
from app.my_project.auth.domain.office import Office

office_bp = Blueprint("office", __name__)
office_dao = OfficeDAO()


@office_bp.get("/")
@swag_from({
    "tags": ["Offices"],
    "summary": "Get all offices",
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
            "description": "List of offices",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"office_id": 1, "office_name": "HQ", "address": "1 Infinite Loop"}
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
def get_all_offices():
    """Return all offices (with optional naive pagination)."""
    offices = office_dao.get_all_offices()
    items = [o.to_dict() for o in offices]

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


@office_bp.get("/<int:id>")
@swag_from({
    "tags": ["Offices"],
    "summary": "Get office by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Office found",
            "content": {
                "application/json": {
                    "example": {"office_id": 1, "office_name": "HQ", "address": "1 Infinite Loop"}
                }
            }
        },
        "404": {"description": "Office not found"}
    }
})
def get_office_by_id(id: int):
    office = office_dao.get_office_by_id(id)
    if office:
        return jsonify(office.to_dict()), 200
    return jsonify({"message": "Office not found"}), 404


@office_bp.post("/")
@swag_from({
    "tags": ["Offices"],
    "summary": "Create office",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["office_name", "address"],
                    "properties": {
                        "office_name": {"type": "string"},
                        "address": {"type": "string"}
                    }
                },
                "example": {
                    "office_name": "Branch A",
                    "address": "221B Baker Street"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Office created"},
        "400": {"description": "Validation error"}
    }
})
def create_office():
    data = request.get_json(silent=True) or {}
    for field in ("office_name", "address"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_office = Office(
            office_name=data["office_name"],
            address=data["address"]
        )
        office_dao.create_office(new_office)
        return jsonify({"message": "Office created successfully", "office_id": getattr(new_office, "office_id", None)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@office_bp.put("/<int:id>")
@swag_from({
    "tags": ["Offices"],
    "summary": "Update office",
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
                        "office_name": {"type": "string"},
                        "address": {"type": "string"}
                    }
                },
                "example": {
                    "office_name": "HQ East",
                    "address": "1600 Amphitheatre Pkwy"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Office updated"},
        "404": {"description": "Office not found"},
        "400": {"description": "Validation error"}
    }
})
def update_office(id: int):
    data = request.get_json(silent=True) or {}
    office = office_dao.get_office_by_id(id)
    if not office:
        return jsonify({"message": "Office not found"}), 404

    try:
        office.office_name = data.get("office_name", office.office_name)
        office.address = data.get("address", office.address)
        office_dao.update_office(office)
        return jsonify({"message": "Office updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@office_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Offices"],
    "summary": "Delete office",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Office deleted"},
        "404": {"description": "Office not found"}
    }
})
def delete_office(id: int):
    office = office_dao.get_office_by_id(id)
    if not office:
        return jsonify({"message": "Office not found"}), 404

    try:
        office_dao.delete_office(office)
        return jsonify({"message": "Office deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@office_bp.get("/<int:id>/employees")
@swag_from({
    "tags": ["Offices"],
    "summary": "Get employees of an office",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Employees for office",
            "content": {
                "application/json": {
                    "example": [
                        {"employee_id": 1, "name": "John", "surname": "Doe", "position": "Dev"}
                    ]
                }
            }
        },
        "404": {"description": "Office not found"}
    }
})
def get_office_employees(id: int):
    office = office_dao.get_office_by_id(id)
    if not office:
        return jsonify({"message": "Office not found"}), 404

    employees = getattr(office, "employees", [])
    return jsonify([e.to_dict() for e in employees]), 200

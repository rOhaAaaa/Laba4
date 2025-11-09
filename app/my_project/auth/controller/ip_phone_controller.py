from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy import text

from app.db import db
from app.my_project.auth.dao.ip_phone_dao import IPPhoneDAO
from app.my_project.auth.domain.ip_phone import IPPhone

ip_phone_bp = Blueprint("ip_phone", __name__)
ip_phone_dao = IPPhoneDAO()


@ip_phone_bp.get("/")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Get all IP phones",
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
            "description": "List of IP phones",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "ip_phone_id": 1,
                                "model_name": "Cisco 7841",
                                "line_type": "SIP",
                                "phone_number": "+1-555-0101"
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
def get_all_ip_phones():
    """Return all IP phones (with optional naive pagination)."""
    ip_phones = ip_phone_dao.get_all_ip_phones()
    items = [p.to_dict() for p in ip_phones]

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


@ip_phone_bp.get("/<int:id>")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Get IP phone by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "IP phone found",
            "content": {
                "application/json": {
                    "example": {
                        "ip_phone_id": 1,
                        "model_name": "Cisco 7841",
                        "line_type": "SIP",
                        "phone_number": "+1-555-0101"
                    }
                }
            }
        },
        "404": {"description": "IP phone not found"}
    }
})
def get_ip_phone_by_id(id: int):
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if ip_phone:
        return jsonify(ip_phone.to_dict()), 200
    return jsonify({"message": "IP Phone not found"}), 404


@ip_phone_bp.post("/")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Create IP phone",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["model_name", "line_type", "phone_number"],
                    "properties": {
                        "model_name": {"type": "string"},
                        "line_type": {"type": "string"},
                        "phone_number": {"type": "string"}
                    }
                },
                "example": {
                    "model_name": "Yealink T46S",
                    "line_type": "SIP",
                    "phone_number": "+380441234567"
                }
            }
        }
    },
    "responses": {
        "201": {"description": "IP phone created"},
        "400": {"description": "Validation error"}
    }
})
def create_ip_phone():
    data = request.get_json(silent=True) or {}
    # валідація
    for field in ("model_name", "line_type", "phone_number"):
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_ip_phone = IPPhone(
            model_name=data["model_name"],
            line_type=data["line_type"],
            phone_number=data["phone_number"]
        )
        ip_phone_dao.add_ip_phone(new_ip_phone)
        return jsonify({"message": "IP Phone created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@ip_phone_bp.put("/<int:id>")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Update IP phone",
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
                        "line_type": {"type": "string"},
                        "phone_number": {"type": "string"}
                    }
                },
                "example": {
                    "model_name": "Cisco 8851",
                    "line_type": "SIP",
                    "phone_number": "+1-555-0202"
                }
            }
        }
    },
    "responses": {
        "200": {"description": "IP phone updated"},
        "404": {"description": "IP phone not found"},
        "400": {"description": "Validation error"}
    }
})
def update_ip_phone(id: int):
    data = request.get_json(silent=True) or {}
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if not ip_phone:
        return jsonify({"message": "IP Phone not found"}), 404

    try:
        ip_phone.model_name = data.get("model_name", ip_phone.model_name)
        ip_phone.line_type = data.get("line_type", ip_phone.line_type)
        ip_phone.phone_number = data.get("phone_number", ip_phone.phone_number)

        ip_phone_dao.update_ip_phone(ip_phone)
        return jsonify({"message": "IP Phone updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@ip_phone_bp.delete("/<int:id>")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Delete IP phone",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "IP phone deleted"},
        "404": {"description": "IP phone not found"}
    }
})
def delete_ip_phone(id: int):
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if not ip_phone:
        return jsonify({"message": "IP Phone not found"}), 404

    try:
        ip_phone_dao.delete_ip_phone(ip_phone)
        return jsonify({"message": "IP Phone deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@ip_phone_bp.post("/add_batch")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Add 10 IP phones via stored procedure",
    "responses": {
        "201": {"description": "10 IP phones added"},
        "500": {"description": "Internal server error"}
    }
})
def add_ip_phone_batch():
    try:
        # Виклик процедури через SQLAlchemy text (без параметрів)
        stmt = text("CALL insert_ip_phone_batch()")
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": "10 IP phones added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@ip_phone_bp.get("/statistic")
@swag_from({
    "tags": ["IP Phones"],
    "summary": "Calculate statistic for a column using DB function",
    "parameters": [
        {
            "name": "column_name",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
            "description": "Column to aggregate (e.g., 'phone_number' length, etc.)"
        },
        {
            "name": "operation",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
            "description": "Operation name expected by DB function (e.g., 'count', 'min', 'max', ...)"
        }
    ],
    "responses": {
        "200": {
            "description": "Calculated statistic",
            "content": {
                "application/json": {
                    "example": {"result": 42}
                }
            }
        },
        "400": {"description": "Validation error"}
    }
})
def get_ip_phone_statistic():
    column_name = request.args.get("column_name")
    operation = request.args.get("operation")

    if not column_name or not operation:
        return jsonify({"error": "Missing column_name or operation"}), 400

    try:
        stmt = text("SELECT calculate_ip_phone_stat(:column_name, :operation) AS result")
        res = db.session.execute(stmt, {
            "column_name": column_name,
            "operation": operation
        })
        row = res.mappings().first() or {}
        return jsonify({"result": row.get("result")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

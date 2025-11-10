from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.db import db
from app.my_project.auth.dao.printer_dao import PrinterDAO
from app.my_project.auth.domain.printer import Printer

printer_bp = Blueprint("printer", __name__)
printer_dao = PrinterDAO()


@printer_bp.get("/")
@swag_from({
    "tags": ["Printers"],
    "summary": "Get all printers",
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
            "description": "List of printers",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"printer_id": 1, "printer_type": "Laser", "print_speed": 35}
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
def get_all_printers():
    """Return all printers (with optional naive pagination)."""
    printers = printer_dao.get_all_printers()
    items = [p.to_dict() for p in printers]

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


@printer_bp.get("/<int:id>")
@swag_from({
    "tags": ["Printers"],
    "summary": "Get printer by ID",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {
            "description": "Printer found",
            "content": {
                "application/json": {
                    "example": {"printer_id": 1, "printer_type": "Laser", "print_speed": 35}
                }
            }
        },
        "404": {"description": "Printer not found"}
    }
})
def get_printer_by_id(id: int):
    printer = printer_dao.get_printer_by_id(id)
    if printer:
        return jsonify(printer.to_dict()), 200
    return jsonify({"message": "Printer not found"}), 404


@printer_bp.post("/")
@swag_from({
    "tags": ["Printers"],
    "summary": "Create printer",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["printer_type", "print_speed"],
                    "properties": {
                        "printer_type": {"type": "string"},
                        "print_speed": {"type": "number", "description": "Pages per minute"}
                    }
                },
                "example": {
                    "printer_type": "Inkjet",
                    "print_speed": 20
                }
            }
        }
    },
    "responses": {
        "201": {"description": "Printer created"},
        "400": {"description": "Validation error"}
    }
})
def create_printer():
    data = request.get_json(silent=True) or {}
    for field in ("printer_type", "print_speed"):
        if not data.get(field) and data.get(field) != 0:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        new_printer = Printer(
            printer_type=data["printer_type"],
            print_speed=data["print_speed"]
        )
        printer_dao.add_printer(new_printer)
        return jsonify({"message": "Printer created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@printer_bp.put("/<int:id>")
@swag_from({
    "tags": ["Printers"],
    "summary": "Update printer",
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
                        "printer_type": {"type": "string"},
                        "print_speed": {"type": "number"}
                    }
                },
                "example": {
                    "printer_type": "Laser",
                    "print_speed": 40
                }
            }
        }
    },
    "responses": {
        "200": {"description": "Printer updated"},
        "404": {"description": "Printer not found"},
        "400": {"description": "Validation error"}
    }
})
def update_printer(id: int):
    data = request.get_json(silent=True) or {}
    printer = printer_dao.get_printer_by_id(id)
    if not printer:
        return jsonify({"message": "Printer not found"}), 404

    try:
        printer.printer_type = data.get("printer_type", printer.printer_type)
        printer.print_speed = data.get("print_speed", printer.print_speed)
        printer_dao.update_printer(printer)
        return jsonify({"message": "Printer updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@printer_bp.delete("/<int:id>")
@swag_from({
    "tags": ["Printers"],
    "summary": "Delete printer",
    "parameters": [
        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
    ],
    "responses": {
        "200": {"description": "Printer deleted"},
        "404": {"description": "Printer not found"}
    }
})
def delete_printer(id: int):
    printer = printer_dao.get_printer_by_id(id)
    if not printer:
        return jsonify({"message": "Printer not found"}), 404

    try:
        printer_dao.delete_printer(printer)
        return jsonify({"message": "Printer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.printer_dao import PrinterDAO
from my_project.auth.domain.printer import Printer

printer_bp = Blueprint('printer', __name__)
printer_dao = PrinterDAO()

@printer_bp.route('/printers', methods=['GET'])
def get_all_printers():
    printers = printer_dao.get_all_printers()
    return jsonify([printer.to_dict() for printer in printers]), 200

@printer_bp.route('/printer/<int:id>', methods=['GET'])
def get_printer_by_id(id):
    printer = printer_dao.get_printer_by_id(id)
    if printer:
        return jsonify(printer.to_dict()), 200
    return jsonify({"message": "Printer not found"}), 404

@printer_bp.route('/printer', methods=['POST'])
def create_printer():
    data = request.get_json()
    try:
        new_printer = Printer(
            printer_type=data['printer_type'],
            print_speed=data['print_speed']
        )
        printer_dao.add_printer(new_printer)
        return jsonify({"message": "Printer created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@printer_bp.route('/printer/<int:id>', methods=['PUT'])
def update_printer(id):
    data = request.get_json()
    printer = printer_dao.get_printer_by_id(id)
    if printer:
        try:
            printer.printer_type = data.get('printer_type', printer.printer_type)
            printer.print_speed = data.get('print_speed', printer.print_speed)
            printer_dao.update_printer(printer)
            return jsonify({"message": "Printer updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Printer not found"}), 404

@printer_bp.route('/printer/<int:id>', methods=['DELETE'])
def delete_printer(id):
    printer = printer_dao.get_printer_by_id(id)
    if printer:
        try:
            printer_dao.delete_printer(printer)
            return jsonify({"message": "Printer deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Printer not found"}), 404

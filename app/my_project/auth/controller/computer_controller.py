import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.computer_dao import ComputerDAO
from my_project.auth.domain.computer import Computer

computer_bp = Blueprint('computer', __name__)
computer_dao = ComputerDAO()

@computer_bp.route('/computers', methods=['GET'])
def get_all_computers():
    computers = computer_dao.get_all_computers()
    return jsonify([computer.to_dict() for computer in computers]), 200

@computer_bp.route('/computer/<int:id>', methods=['GET'])
def get_computer_by_id(id):
    computer = computer_dao.get_computer_by_id(id)
    if computer:
        return jsonify(computer.to_dict()), 200
    return jsonify({"message": "Computer not found"}), 404

@computer_bp.route('/computer', methods=['POST'])
def create_computer():
    data = request.get_json()
    try:
        if 'model_name' not in data or 'operating_system' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_computer = Computer(
            model_name=data['model_name'],
            operating_system=data['operating_system'],
            config_id=data.get('config_id')  
        )
        computer_dao.add_computer(new_computer)
        return jsonify({"message": "Computer created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@computer_bp.route('/computer/<int:id>', methods=['PUT'])
def update_computer(id):
    data = request.get_json()
    computer = computer_dao.get_computer_by_id(id)
    if computer:
        try:
            computer.model_name = data.get('model_name', computer.model_name)
            computer.operating_system = data.get('operating_system', computer.operating_system)
            computer.config_id = data.get('config_id', computer.config_id)
            computer_dao.update_computer(computer)
            return jsonify({"message": "Computer updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Computer not found"}), 404

@computer_bp.route('/computer/<int:id>', methods=['DELETE'])
def delete_computer(id):
    computer = computer_dao.get_computer_by_id(id)
    if computer:
        try:
            computer_dao.delete_computer(computer)
            return jsonify({"message": "Computer deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete computer: {str(e)}"}), 500
    return jsonify({"message": "Computer not found"}), 404

@computer_bp.route('/computers_with_configurations', methods=['GET'])
def get_computers_with_configurations():
    computers = computer_dao.get_all_computers()
    computers_with_configs = [
        {
            'computer_id': computer.computer_id,
            'model_name': computer.model_name,
            'operating_system': computer.operating_system,
            'configuration': computer.configuration.to_dict() if computer.configuration else None
        }
        for computer in computers
    ]
    return jsonify(computers_with_configs), 200


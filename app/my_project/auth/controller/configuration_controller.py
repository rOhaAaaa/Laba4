import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.configuration_dao import ConfigurationDAO
from my_project.auth.domain.configuration import Configuration

configuration_bp = Blueprint('configuration', __name__)
configuration_dao = ConfigurationDAO()

@configuration_bp.route('/configurations', methods=['GET'])
def get_all_configurations():
    configurations = configuration_dao.get_all_configurations()
    return jsonify([configuration.to_dict() for configuration in configurations]), 200

@configuration_bp.route('/configuration/<int:id>', methods=['GET'])
def get_configuration_by_id(id):
    configuration = configuration_dao.get_configuration_by_id(id)
    if configuration:
        return jsonify(configuration.to_dict()), 200
    return jsonify({"message": "Configuration not found"}), 404

@configuration_bp.route('/configuration', methods=['POST'])
def create_configuration():
    data = request.get_json()
    try:
        if 'processor' not in data or 'ram' not in data or 'hard_drive' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_configuration = Configuration(
            processor=data['processor'],
            ram=data['ram'],
            hard_drive=data['hard_drive']
        )
        configuration_dao.add_configuration(new_configuration)
        return jsonify({"message": "Configuration created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@configuration_bp.route('/configuration/<int:id>', methods=['PUT'])
def update_configuration(id):
    data = request.get_json()
    configuration = configuration_dao.get_configuration_by_id(id)
    if configuration:
        try:
            if 'processor' not in data and 'ram' not in data and 'hard_drive' not in data:
                return jsonify({"error": "No data provided to update"}), 400

            configuration.processor = data.get('processor', configuration.processor)
            configuration.ram = data.get('ram', configuration.ram)
            configuration.hard_drive = data.get('hard_drive', configuration.hard_drive)
            configuration_dao.update_configuration(configuration)
            return jsonify({"message": "Configuration updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Configuration not found"}), 404

@configuration_bp.route('/configuration/<int:id>', methods=['DELETE'])
def delete_configuration(id):
    configuration = configuration_dao.get_configuration_by_id(id)
    if configuration:
        try:
            configuration_dao.delete_configuration(configuration)
            return jsonify({"message": "Configuration deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete configuration: {str(e)}"}), 500
    return jsonify({"message": "Configuration not found"}), 404

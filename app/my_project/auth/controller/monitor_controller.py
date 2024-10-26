import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.monitor_dao import MonitorDAO
from my_project.auth.domain.monitor import Monitor

monitor_bp = Blueprint('monitor', __name__)
monitor_dao = MonitorDAO()

@monitor_bp.route('/monitors', methods=['GET'])
def get_all_monitors():
    monitors = monitor_dao.get_all_monitors()
    return jsonify([monitor.to_dict() for monitor in monitors]), 200

@monitor_bp.route('/monitor/<int:id>', methods=['GET'])
def get_monitor_by_id(id):
    monitor = monitor_dao.get_monitor_by_id(id)
    if monitor:
        return jsonify(monitor.to_dict()), 200
    return jsonify({"message": "Monitor not found"}), 404

@monitor_bp.route('/monitor', methods=['POST'])
def create_monitor():
    data = request.get_json()
    try:
        if 'model_name' not in data or 'screen_size' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_monitor = Monitor(
            model_name=data['model_name'],
            screen_size=data['screen_size']
        )
        monitor_dao.add_monitor(new_monitor)
        return jsonify({"message": "Monitor created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitor_bp.route('/monitor/<int:id>', methods=['PUT'])
def update_monitor(id):
    data = request.get_json()
    monitor = monitor_dao.get_monitor_by_id(id)
    if monitor:
        try:
            monitor.model_name = data.get('model_name', monitor.model_name)
            monitor.screen_size = data.get('screen_size', monitor.screen_size)
            monitor_dao.update_monitor(monitor)
            return jsonify({"message": "Monitor updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Monitor not found"}), 404

@monitor_bp.route('/monitor/<int:id>', methods=['DELETE'])
def delete_monitor(id):
    monitor = monitor_dao.get_monitor_by_id(id)
    if monitor:
        try:
            monitor_dao.delete_monitor(monitor)
            return jsonify({"message": "Monitor deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Monitor not found"}), 404

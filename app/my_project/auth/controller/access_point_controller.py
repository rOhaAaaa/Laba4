import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.access_point_dao import AccessPointDAO
from my_project.auth.domain.access_point import AccessPoint

access_point_bp = Blueprint('access_point', __name__)
access_point_dao = AccessPointDAO()

@access_point_bp.route('/access_points', methods=['GET'])
def get_all_access_points():
    access_points = access_point_dao.get_all_access_points()
    return jsonify([access_point.to_dict() for access_point in access_points]), 200

@access_point_bp.route('/access_point/<int:id>', methods=['GET'])
def get_access_point_by_id(id):
    access_point = access_point_dao.get_access_point_by_id(id)
    if access_point:
        return jsonify(access_point.to_dict()), 200
    return jsonify({"message": "Access Point not found"}), 404

@access_point_bp.route('/access_point', methods=['POST'])
def create_access_point():
    data = request.get_json()
    try:
        if 'brand' not in data or 'model' not in data or 'serial_number' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_access_point = AccessPoint(
            brand=data['brand'],
            model=data['model'],
            serial_number=data['serial_number'],
        )
        result = access_point_dao.create_access_point(new_access_point)
        if result['success']:
            return jsonify({"message": "Access Point created successfully"}), 201
        else:
            return jsonify({"error": result['error']}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@access_point_bp.route('/access_point/<int:id>', methods=['PUT'])
def update_access_point(id):
    data = request.get_json()
    access_point = access_point_dao.get_access_point_by_id(id)
    if access_point:
        try:
            access_point.brand = data.get('brand', access_point.brand)
            access_point.model = data.get('model', access_point.model)
            access_point.serial_number = data.get('serial_number', access_point.serial_number)
            result = access_point_dao.update_access_point(access_point)
            if result['success']:
                return jsonify({"message": "Access Point updated successfully"}), 200
            else:
                return jsonify({"error": result['error']}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Access Point not found"}), 404

@access_point_bp.route('/access_point/<int:id>', methods=['DELETE'])
def delete_access_point(id):
    access_point = access_point_dao.get_access_point_by_id(id)
    if access_point:
        try:
            result = access_point_dao.delete_access_point(access_point)
            if result['success']:
                return jsonify({"message": "Access Point deleted successfully"}), 200
            else:
                return jsonify({"error": result['error']}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Access Point not found"}), 404

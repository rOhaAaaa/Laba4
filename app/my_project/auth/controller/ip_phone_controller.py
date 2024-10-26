import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.ip_phone_dao import IPPhoneDAO
from my_project.auth.domain.ip_phone import IPPhone

ip_phone_bp = Blueprint('ip_phone', __name__)
ip_phone_dao = IPPhoneDAO()

@ip_phone_bp.route('/ip_phones', methods=['GET'])
def get_all_ip_phones():
    ip_phones = ip_phone_dao.get_all_ip_phones()
    return jsonify([ip_phone.to_dict() for ip_phone in ip_phones]), 200

@ip_phone_bp.route('/ip_phone/<int:id>', methods=['GET'])
def get_ip_phone_by_id(id):
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if ip_phone:
        return jsonify(ip_phone.to_dict()), 200
    return jsonify({"message": "IP Phone not found"}), 404

@ip_phone_bp.route('/ip_phone', methods=['POST'])
def create_ip_phone():
    data = request.get_json()
    try:
        # Перевіряємо, щоб всі необхідні поля були передані
        if 'model_name' not in data or 'line_type' not in data or 'phone_number' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_ip_phone = IPPhone(
            model_name=data['model_name'],
            line_type=data['line_type'],
            phone_number=data['phone_number']
        )
        ip_phone_dao.add_ip_phone(new_ip_phone)  # Використовуємо add_ip_phone замість create_ip_phone
        return jsonify({"message": "IP Phone created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ip_phone_bp.route('/ip_phone/<int:id>', methods=['PUT'])
def update_ip_phone(id):
    data = request.get_json()
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if ip_phone:
        try:
            ip_phone.model_name = data.get('model_name', ip_phone.model_name)
            ip_phone.line_type = data.get('line_type', ip_phone.line_type)
            ip_phone.phone_number = data.get('phone_number', ip_phone.phone_number)
            ip_phone_dao.update_ip_phone(ip_phone)
            return jsonify({"message": "IP Phone updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "IP Phone not found"}), 404

@ip_phone_bp.route('/ip_phone/<int:id>', methods=['DELETE'])
def delete_ip_phone(id):
    ip_phone = ip_phone_dao.get_ip_phone_by_id(id)
    if ip_phone:
        try:
            ip_phone_dao.delete_ip_phone(ip_phone)
            return jsonify({"message": "IP Phone deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "IP Phone not found"}), 404

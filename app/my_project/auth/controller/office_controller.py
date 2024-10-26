# my_project/auth/controller/office_controller.py
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.office_dao import OfficeDAO
from my_project.auth.domain.office import Office

office_bp = Blueprint('office', __name__)
office_dao = OfficeDAO()

@office_bp.route('/', methods=['GET'])
def get_all_offices():
    offices = office_dao.get_all_offices()
    return jsonify([office.to_dict() for office in offices]), 200

@office_bp.route('/<int:id>', methods=['GET'])
def get_office_by_id(id):
    office = office_dao.get_office_by_id(id)
    if office:
        return jsonify(office.to_dict()), 200
    return jsonify({"message": "Office not found"}), 404

@office_bp.route('/', methods=['POST'])
def create_office():
    data = request.get_json()
    try:
        new_office = Office(
            office_name=data['office_name'],
            address=data['address']
        )
        office_dao.create_office(new_office)
        return jsonify({"message": "Office created successfully", "office_id": new_office.office_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@office_bp.route('/<int:id>', methods=['PUT'])
def update_office(id):
    data = request.get_json()
    office = office_dao.get_office_by_id(id)
    if office:
        try:
            office.office_name = data.get('office_name', office.office_name)
            office.address = data.get('address', office.address)
            office_dao.update_office(office)
            return jsonify({"message": "Office updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Office not found"}), 404

@office_bp.route('/<int:id>', methods=['DELETE'])
def delete_office(id):
    office = office_dao.get_office_by_id(id)
    if office:
        try:
            office_dao.delete_office(office)
            return jsonify({"message": "Office deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Office not found"}), 404

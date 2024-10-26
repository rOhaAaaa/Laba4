import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from my_project.auth.dao.router_dao import RouterDAO
from my_project.auth.domain.router import Router

router_bp = Blueprint('router', __name__)
router_dao = RouterDAO()

@router_bp.route('/routers', methods=['GET'])
def get_all_routers():
    routers = router_dao.get_all_routers()
    return jsonify([router.to_dict() for router in routers]), 200

@router_bp.route('/router/<int:id>', methods=['GET'])
def get_router_by_id(id):
    router = router_dao.get_router_by_id(id)
    if router:
        return jsonify(router.to_dict()), 200
    return jsonify({"message": "Router not found"}), 404

@router_bp.route('/router', methods=['POST'])
def create_router():
    data = request.get_json()
    try:
        new_router = Router(
            model_name=data['model_name'],
            connection_speed=data['connection_speed']  # Змінив `speed` на `connection_speed`
        )
        router_dao.add_router(new_router)  # Змінив `create_router()` на `add_router()`
        return jsonify({"message": "Router created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@router_bp.route('/router/<int:id>', methods=['PUT'])
def update_router(id):
    data = request.get_json()
    router = router_dao.get_router_by_id(id)
    if router:
        try:
            router.model_name = data.get('model_name', router.model_name)
            router.connection_speed = data.get('connection_speed', router.connection_speed)  # Змінив `speed` на `connection_speed`
            router_dao.update_router(router)
            return jsonify({"message": "Router updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Router not found"}), 404

@router_bp.route('/router/<int:id>', methods=['DELETE'])
def delete_router(id):
    router = router_dao.get_router_by_id(id)
    if router:
        try:
            router_dao.delete_router(router)
            return jsonify({"message": "Router deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Router not found"}), 404

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Blueprint, request, jsonify
from app.my_project.auth.service.generic_service import GenericService

procedure_bp = Blueprint('procedure', __name__)
service = GenericService()

@procedure_bp.route('/procedure/<procedure_name>', methods=['POST'])
def call_procedure(procedure_name):
    try:
        params = request.json.get('params', [])

        results = service.execute_procedure(procedure_name, params)
        return jsonify({"message": "Procedure executed", "results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

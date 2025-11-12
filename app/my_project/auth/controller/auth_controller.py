from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin":
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200

    return jsonify(message="Bad credentials"), 401

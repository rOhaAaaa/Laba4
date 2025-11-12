import os
import time
import math
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from .db import db


def create_app():
    app = Flask(__name__)

    db_url = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("DATABASE_URL")
        or "mysql+pymysql://app_user:password@127.0.0.1:3306/app_db"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["DEBUG"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change_me")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change_me_too")

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    swagger_template = {
        "swagger": "2.0",
        "info": {"title": "Laba 4 API", "version": "1.0.0"},
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT header: Bearer {token}",
            }
        },
    }
    app.config["SWAGGER"] = {
        "title": "Laba 4 API",
        "uiversion": 3,
        "specs_route": "/apidocs/",
    }
    Swagger(app, template=swagger_template)

    from .my_project.auth.controller.employee_controller import employee_bp
    from .my_project.auth.controller.office_controller import office_bp
    from .my_project.auth.controller.configuration_controller import configuration_bp
    from .my_project.auth.controller.computer_controller import computer_bp
    from .my_project.auth.controller.monitor_controller import monitor_bp
    from .my_project.auth.controller.printer_controller import printer_bp
    from .my_project.auth.controller.access_point_controller import access_point_bp
    from .my_project.auth.controller.router_controller import router_bp
    from .my_project.auth.controller.employee_equipment_controller import (
        employee_equipment_bp,
    )
    from .my_project.auth.controller.ip_phone_controller import ip_phone_bp
    from .my_project.auth.controller.departments_controller import department_bp
    from .my_project.auth.controller.procedure_controller import procedure_bp

    app.register_blueprint(employee_bp, url_prefix="/employees")
    app.register_blueprint(office_bp, url_prefix="/offices")
    app.register_blueprint(configuration_bp, url_prefix="/configurations")
    app.register_blueprint(computer_bp, url_prefix="/computers")
    app.register_blueprint(monitor_bp, url_prefix="/monitors")
    app.register_blueprint(printer_bp, url_prefix="/printers")
    app.register_blueprint(access_point_bp, url_prefix="/access_points")
    app.register_blueprint(router_bp, url_prefix="/routers")
    app.register_blueprint(employee_equipment_bp, url_prefix="/employee_equipment")
    app.register_blueprint(ip_phone_bp, url_prefix="/ip_phone")
    app.register_blueprint(department_bp, url_prefix="/departments")
    app.register_blueprint(procedure_bp, url_prefix="/procedures")

    @app.get("/")
    def home():
        return "Welcome to the Laba 4 API!"

    @app.get("/heavy")
    def heavy():
        """
        Heavy endpoint (CPU or sleep)
        ---
        parameters:
          - name: seconds
            in: query
            type: number
            required: false
            default: 3
            description: Seconds to simulate work (0.1–60)
          - name: mode
            in: query
            type: string
            required: false
            default: cpu
            enum: [cpu, sleep]
            description: Work mode: CPU-intensive (cpu) or blocking sleep (sleep)
        responses:
          200:
            description: Work finished
        """
        try:
            seconds = float(request.args.get("seconds", 3))
        except ValueError:
            seconds = 3.0
        seconds = max(0.1, min(60.0, seconds))

        mode = request.args.get("mode", "cpu").strip().lower()

        started = time.time()
        if mode == "sleep":
            time.sleep(seconds)
            elapsed = time.time() - started
            return jsonify(ok=True, mode="sleep", slept=round(seconds, 3), elapsed=round(elapsed, 3))
        else:
            end = started + seconds
            junk = 0.0
            i = 0
            while time.time() < end:
                i += 1
                junk += math.sqrt((i % 1000) + 0.123) * math.sin(i * 0.001)
                if i % 100000 == 0:
                    junk = junk / 2.0
            elapsed = time.time() - started
            return jsonify(ok=True, mode="cpu", elapsed=round(elapsed, 3), iters=i, junk=round(junk, 6))

    return app


app = create_app()

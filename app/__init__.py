import sys
import os

# Додаємо шлях до папки 'app', щоб модулі були доступні
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from db import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:5555@localhost/mybd1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True  

    db.init_app(app)
    migrate = Migrate(app, db)

    # Реєстрація blueprints для кожного контролера
    from my_project.auth.controller.employee_controller import employee_bp
    from my_project.auth.controller.office_controller import office_bp
    from my_project.auth.controller.configuration_controller import configuration_bp
    from my_project.auth.controller.computer_controller import computer_bp
    from my_project.auth.controller.monitor_controller import monitor_bp
    from my_project.auth.controller.printer_controller import printer_bp
    from my_project.auth.controller.access_point_controller import access_point_bp
    from my_project.auth.controller.router_controller import router_bp
    from my_project.auth.controller.employee_equipment_controller import employee_equipment_bp
    from my_project.auth.controller.ip_phone_controller import ip_phone_bp

    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(office_bp, url_prefix='/offices')
    app.register_blueprint(configuration_bp, url_prefix='/configurations')  
    app.register_blueprint(computer_bp, url_prefix='/computers')
    app.register_blueprint(monitor_bp, url_prefix='/monitors')
    app.register_blueprint(printer_bp, url_prefix='/printers')
    app.register_blueprint(access_point_bp, url_prefix='/access_points')
    app.register_blueprint(router_bp, url_prefix='/routers')
    app.register_blueprint(employee_equipment_bp, url_prefix='/employee_equipment')
    app.register_blueprint(ip_phone_bp, url_prefix='/ip_phone')

    @app.route('/')
    def home():
        return "Welcome to the Laba 4 API!"

    return app

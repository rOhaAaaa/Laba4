from app.db import db

employee_printers = db.Table(
    'employee_printers',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True),
    db.Column('printer_id', db.Integer, db.ForeignKey('printers.printer_id'), primary_key=True)
)

employee_projects = db.Table(
    'employee_projects',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.project_id'), primary_key=True)
)
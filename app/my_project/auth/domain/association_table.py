from db import db

employee_printers = db.Table(
    'employee_printers',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True),
    db.Column('printer_id', db.Integer, db.ForeignKey('printers.printer_id'), primary_key=True)
)

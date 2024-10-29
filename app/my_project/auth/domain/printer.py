from db import db
from sqlalchemy.orm import relationship
from my_project.auth.domain.association_table import employee_printers

class Printer(db.Model):
    __tablename__ = 'printers'

    printer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    printer_type = db.Column(db.String(50), nullable=False)
    print_speed = db.Column(db.String(50), nullable=False)

    employees = relationship('Employee', secondary=employee_printers, back_populates='printers')

    def to_dict(self):
        return {
            'printer_id': self.printer_id,
            'printer_type': self.printer_type,
            'print_speed': self.print_speed,
            'employees': [employee.to_dict() for employee in self.employees]
        }

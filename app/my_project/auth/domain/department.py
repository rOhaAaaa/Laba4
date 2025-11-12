from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import db

class Department(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)

    employees = relationship('Employee', back_populates='department')

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name,
            'employees': [employee.to_dict() for employee in self.employees]
        }
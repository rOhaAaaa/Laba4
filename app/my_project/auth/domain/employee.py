from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db

class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.office_id'), nullable=True)
    office = db.relationship("Office", back_populates="employees")

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'surname': self.surname,
            'position': self.position,
            'office_id': self.office_id
        }

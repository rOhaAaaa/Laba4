from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import db
from app.my_project.auth.domain.association_table import employee_projects

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    employees = relationship('Employee', secondary=employee_projects, back_populates='projects') 

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'description': self.description,
            'employees': [employee.to_dict() for employee in self.employees]
        }

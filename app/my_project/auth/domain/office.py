from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db

class Office(db.Model):
    __tablename__ = 'offices'

    office_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    office_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Вказання відносин з іншими таблицями
    employees = relationship("Employee", back_populates="office", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'office_id': self.office_id,
            'office_name': self.office_name,
            'address': self.address
        }

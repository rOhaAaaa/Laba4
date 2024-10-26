from sqlalchemy import Column, Integer, String
from db import db

class AccessPoint(db.Model):
    __tablename__ = 'access_points'

    access_point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)  

    def to_dict(self):
        return {
            'access_point_id': self.access_point_id,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
        }

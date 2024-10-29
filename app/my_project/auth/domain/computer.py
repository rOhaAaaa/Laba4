from db import db
from sqlalchemy.orm import relationship


class Computer(db.Model):
    __tablename__ = 'computers'

    computer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    operating_system = db.Column(db.String(100), nullable=False)
    config_id = db.Column(db.Integer, db.ForeignKey('configurations.config_id'))  
    
    configuration = relationship("Configuration", backref="computers")

    def to_dict(self):
        return {
            'computer_id': self.computer_id,
            'model_name': self.model_name,
            'operating_system': self.operating_system,
            'config_id': self.config_id,
            'configuration': self.configuration.to_dict() if self.configuration else None
        }

from db import db

class Computer(db.Model):
    __tablename__ = 'computers'

    computer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    operating_system = db.Column(db.String(100), nullable=False)
    config_id = db.Column(db.Integer)  
    
    def to_dict(self):
        return {
            'computer_id': self.computer_id,
            'model_name': self.model_name,
            'operating_system': self.operating_system,
            'config_id': self.config_id
        }

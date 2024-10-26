from db import db

class Configuration(db.Model):
    __tablename__ = 'configurations'

    config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    processor = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(50), nullable=False)
    hard_drive = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'config_id': self.config_id,
            'processor': self.processor,
            'ram': self.ram,
            'hard_drive': self.hard_drive
        }

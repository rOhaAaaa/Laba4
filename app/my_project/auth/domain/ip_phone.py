from db import db

class IPPhone(db.Model):
    __tablename__ = 'ip_phones'

    phone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    line_type = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False) 

    def to_dict(self):
        return {
            'phone_id': self.phone_id,
            'model_name': self.model_name,
            'line_type': self.line_type,
            'phone_number': self.phone_number
        }

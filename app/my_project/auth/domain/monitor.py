from db import db

class Monitor(db.Model):
    __tablename__ = 'monitors'

    monitor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    screen_size = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'monitor_id': self.monitor_id,
            'model_name': self.model_name,
            'screen_size': self.screen_size
        }

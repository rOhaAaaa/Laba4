from db import db

class Router(db.Model):
    __tablename__ = 'routers'

    router_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    connection_speed = db.Column(db.String(50), nullable=False)
    

    def to_dict(self):
        return {
            'router_id': self.router_id,
            'model_name': self.model_name,
            'connection_speed': self.connection_speed
        }

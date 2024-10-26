from my_project.auth.domain.monitor import Monitor
from db import db

class MonitorDAO:
    def __init__(self):
        pass

    def get_all_monitors(self):
        return Monitor.query.all()

    def get_monitor_by_id(self, monitor_id: int):
        return Monitor.query.get(monitor_id)

    def add_monitor(self, monitor: Monitor):
        try:
            db.session.add(monitor)
            db.session.commit()
            db.session.refresh(monitor)
            return monitor
        except Exception as e:
            db.session.rollback()
            raise e

    def update_monitor(self, monitor):
        try:
            db.session.commit()
            db.session.refresh(monitor)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_monitor(self, monitor):
        try:
            db.session.delete(monitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

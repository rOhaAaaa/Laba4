from my_project.auth.dao.monitor_dao import MonitorDAO

class MonitorService:
    def __init__(self):
        self.monitor_dao = MonitorDAO()

    def get_all_monitors(self):
        return self.monitor_dao.get_all_monitors()

    def get_monitor_by_id(self, monitor_id):
        return self.monitor_dao.get_monitor_by_id(monitor_id)

    def create_monitor(self, data):
        return self.monitor_dao.create_monitor(data)

    def update_monitor(self, monitor_id, data):
        return self.monitor_dao.update_monitor(monitor_id, data)

    def delete_monitor(self, monitor_id):
        return self.monitor_dao.delete_monitor(monitor_id)

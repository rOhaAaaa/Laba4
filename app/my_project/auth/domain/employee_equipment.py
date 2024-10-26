from db import db

class EmployeeEquipment(db.Model):
    __tablename__ = 'employee_equipment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.computer_id'), nullable=False)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.monitor_id'), nullable=False)
    phone_id = db.Column(db.Integer, db.ForeignKey('ip_phones.phone_id'), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.office_id'), nullable=False)
    printer_id = db.Column(db.Integer, db.ForeignKey('printers.printer_id'), nullable=False)
    router_id = db.Column(db.Integer, db.ForeignKey('routers.router_id'), nullable=False)
    access_point_id = db.Column(db.Integer, db.ForeignKey('access_points.access_point_id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'computer_id': self.computer_id,
            'monitor_id': self.monitor_id,
            'phone_id': self.phone_id,
            'office_id': self.office_id,
            'printer_id': self.printer_id,
            'router_id': self.router_id,
            'access_point_id': self.access_point_id,
            'issue_date': self.issue_date.isoformat()
        }

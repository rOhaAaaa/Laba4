from my_project.auth.domain.printer import Printer
from db import db

class PrinterDAO:
    def __init__(self):
        pass

    def get_all_printers(self):
        return Printer.query.all()

    def get_printer_by_id(self, printer_id: int):
        return Printer.query.get(printer_id)

    def add_printer(self, printer: Printer):
        try:
            db.session.add(printer)
            db.session.commit()
            db.session.refresh(printer)
            return printer
        except Exception as e:
            db.session.rollback()
            raise e

    def update_printer(self, printer):
        try:
            db.session.commit()
            db.session.refresh(printer)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_printer(self, printer):
        try:
            db.session.delete(printer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

from my_project.auth.dao.printer_dao import PrinterDAO

class PrinterService:
    def __init__(self):
        self.printer_dao = PrinterDAO()

    def get_all_printers(self):
        return self.printer_dao.get_all_printers()

    def get_printer_by_id(self, printer_id):
        return self.printer_dao.get_printer_by_id(printer_id)

    def create_printer(self, data):
        return self.printer_dao.create_printer(data)

    def update_printer(self, printer_id, data):
        return self.printer_dao.update_printer(printer_id, data)

    def delete_printer(self, printer_id):
        return self.printer_dao.delete_printer(printer_id)

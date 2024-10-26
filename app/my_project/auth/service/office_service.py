from my_project.auth.dao.office_dao import OfficeDAO

class OfficeService:
    def __init__(self):
        self.office_dao = OfficeDAO()

    def get_all_offices(self):
        return self.office_dao.get_all_offices()

    def get_office_by_id(self, office_id):
        return self.office_dao.get_office_by_id(office_id)

    def create_office(self, data):
        return self.office_dao.create_office(data)

    def update_office(self, office_id, data):
        return self.office_dao.update_office(office_id, data)

    def delete_office(self, office_id):
        return self.office_dao.delete_office(office_id)

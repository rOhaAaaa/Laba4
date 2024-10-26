from my_project.auth.dao.computer_dao import ComputerDAO

class ComputerService:
    def __init__(self):
        self.computer_dao = ComputerDAO()

    def get_all_computers(self):
        return self.computer_dao.get_all_computers()

    def get_computer_by_id(self, computer_id):
        return self.computer_dao.get_computer_by_id(computer_id)

    def create_computer(self, data):
        return self.computer_dao.create_computer(data)

    def update_computer(self, computer_id, data):
        return self.computer_dao.update_computer(computer_id, data)

    def delete_computer(self, computer_id):
        return self.computer_dao.delete_computer(computer_id)

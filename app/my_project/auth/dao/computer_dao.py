from my_project.auth.domain.computer import Computer
from db import db

class ComputerDAO:
    def __init__(self):
        pass

    def get_all_computers(self):
        return Computer.query.all()

    def get_computer_by_id(self, computer_id: int):
        return Computer.query.get(computer_id)

    def add_computer(self, computer: Computer):
        try:
            db.session.add(computer)
            db.session.commit()
            db.session.refresh(computer)
            return computer
        except Exception as e:
            db.session.rollback()
            raise e

    def update_computer(self, computer):
        try:
            db.session.commit()
            db.session.refresh(computer)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_computer(self, computer):
        try:
            db.session.delete(computer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

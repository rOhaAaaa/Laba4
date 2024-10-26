from my_project.auth.domain.office import Office
from db import db

class OfficeDAO:
    def __init__(self):
        pass

    def get_all_offices(self):
        return Office.query.all()

    def get_office_by_id(self, id):
        return Office.query.get(id)

    def create_office(self, office):
        try:
            db.session.add(office)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_office(self, office):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_office(self, office):
        try:
            db.session.delete(office)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

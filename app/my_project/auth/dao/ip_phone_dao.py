from my_project.auth.domain.ip_phone import IPPhone
from db import db

class IPPhoneDAO:
    def __init__(self):
        pass

    def get_all_ip_phones(self):
        return IPPhone.query.all()

    def get_ip_phone_by_id(self, phone_id: int):
        return IPPhone.query.get(phone_id)

    def add_ip_phone(self, ip_phone: IPPhone):
        try:
            db.session.add(ip_phone)
            db.session.commit()
            db.session.refresh(ip_phone)
            return ip_phone
        except Exception as e:
            db.session.rollback()
            raise e

    def update_ip_phone(self, ip_phone):
        try:
            db.session.commit()
            db.session.refresh(ip_phone)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_ip_phone(self, ip_phone):
        try:
            db.session.delete(ip_phone)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

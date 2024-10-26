from my_project.auth.dao.ip_phone_dao import IPPhoneDAO

class IPPhoneService:
    def __init__(self):
        self.ip_phone_dao = IPPhoneDAO()

    def get_all_ip_phones(self):
        return self.ip_phone_dao.get_all_ip_phones()

    def get_ip_phone_by_id(self, phone_id):
        return self.ip_phone_dao.get_ip_phone_by_id(phone_id)

    def create_ip_phone(self, data):
        return self.ip_phone_dao.create_ip_phone(data)

    def update_ip_phone(self, phone_id, data):
        return self.ip_phone_dao.update_ip_phone(phone_id, data)

    def delete_ip_phone(self, phone_id):
        return self.ip_phone_dao.delete_ip_phone(phone_id)

from my_project.auth.dao.access_point_dao import AccessPointDAO

class AccessPointService:
    def __init__(self):
        self.access_point_dao = AccessPointDAO()

    def get_all_access_points(self):
        return self.access_point_dao.get_all_access_points()

    def get_access_point_by_id(self, access_point_id):
        return self.access_point_dao.get_access_point_by_id(access_point_id)

    def create_access_point(self, data):
        return self.access_point_dao.create_access_point(data)

    def update_access_point(self, access_point_id, data):
        return self.access_point_dao.update_access_point(access_point_id, data)

    def delete_access_point(self, access_point_id):
        return self.access_point_dao.delete_access_point(access_point_id)

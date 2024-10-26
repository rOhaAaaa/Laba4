from my_project.auth.dao.router_dao import RouterDAO

class RouterService:
    def __init__(self):
        self.router_dao = RouterDAO()

    def get_all_routers(self):
        return self.router_dao.get_all_routers()

    def get_router_by_id(self, router_id):
        return self.router_dao.get_router_by_id(router_id)

    def create_router(self, data):
        return self.router_dao.create_router(data)

    def update_router(self, router_id, data):
        return self.router_dao.update_router(router_id, data)

    def delete_router(self, router_id):
        return self.router_dao.delete_router(router_id)

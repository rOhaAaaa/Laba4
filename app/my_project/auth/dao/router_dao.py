from my_project.auth.domain.router import Router
from db import db

class RouterDAO:
    def __init__(self):
        pass

    def get_all_routers(self):
        return Router.query.all()

    def get_router_by_id(self, router_id: int):
        return Router.query.get(router_id)

    def add_router(self, router: Router):
        try:
            db.session.add(router)
            db.session.commit()
            db.session.refresh(router)
            return router
        except Exception as e:
            db.session.rollback()
            raise e

    def update_router(self, router):
        try:
            db.session.commit()
            db.session.refresh(router)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_router(self, router):
        try:
            db.session.delete(router)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

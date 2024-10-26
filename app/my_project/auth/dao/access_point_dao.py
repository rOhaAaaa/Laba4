from my_project.auth.domain.access_point import AccessPoint
from db import db

class AccessPointDAO:
    def __init__(self):
        pass

    def get_all_access_points(self) -> list[AccessPoint]:
        return AccessPoint.query.all()

    def get_access_point_by_id(self, access_point_id: int) -> AccessPoint:
        return AccessPoint.query.get(access_point_id)

    def create_access_point(self, access_point: AccessPoint) -> dict:
        try:
            db.session.add(access_point)
            db.session.commit()
            db.session.refresh(access_point)
            return {"success": True, "data": access_point}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    def update_access_point(self, access_point: AccessPoint) -> dict:
        try:
            db.session.commit()
            db.session.refresh(access_point)
            return {"success": True, "data": access_point}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    def delete_access_point(self, access_point: AccessPoint) -> dict:
        try:
            db.session.delete(access_point)
            db.session.commit()
            return {"success": True}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

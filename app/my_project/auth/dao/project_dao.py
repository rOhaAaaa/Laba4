from my_project.auth.domain.project import Project
from db import db

class ProjectDAO:
    def __init__(self):
        pass

    def get_all_projects(self):
        return Project.query.all()

    def get_project_by_id(self, project_id: int):
        return Project.query.get(project_id)

    def create_project(self, project: Project):
        try:
            db.session.add(project)
            db.session.commit()
            db.session.refresh(project)
            return project
        except Exception as e:
            db.session.rollback()
            raise e

    def update_project(self, project):
        try:
            db.session.commit()
            db.session.refresh(project)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_project(self, project):
        try:
            db.session.delete(project)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
